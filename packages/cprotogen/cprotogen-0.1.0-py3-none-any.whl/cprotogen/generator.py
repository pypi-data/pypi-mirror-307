"""Generator module for the library."""

import argparse
import os.path
import re

import pycparser_fake_libc
from pycparser import c_ast, c_generator, parse_file


class BaseVisitor(c_ast.NodeVisitor):
    """Base ast visitor class."""

    def __init__(self) -> None:
        """Init method."""
        self.protos: list[str] = []
        self.protos_map: dict[str, str] = {}
        self._generator = c_generator.CGenerator()
        # if you have more than 10**15 loc in a single file
        # you might want to refactor it a bit
        self.first_proto_line_no = 10**15
        self.last_proto_line_no = 0


class HeaderVisitor(BaseVisitor):
    """The Header visitor class."""

    def visit_FuncDecl(self, node: c_ast.FuncDecl) -> None:  # noqa: N802
        """Extract the prototype and the function name from the declaration."""
        self.first_proto_line_no = min(self.first_proto_line_no, node.coord.line)
        self.last_proto_line_no = max(self.last_proto_line_no, node.coord.line)

        proto = self._generator.visit(node)
        tp = self._generator.visit(node.type)

        tp_escaped = re.escape(tp.strip())
        fn_name = re.search(rf"{tp_escaped}\s*(\w+)\s*\(", proto).group(1)  # type: ignore[union-attr]

        proto += ";"  # generator removes the trailing ;

        self.protos_map[fn_name] = proto
        self.protos.append(proto)


class SourceVisitor(BaseVisitor):
    """The Source file visitor class."""

    def visit_FuncDef(self, node: c_ast.FuncDef) -> None:  # noqa: N802
        """Extract the function prototype from its definition."""
        self.first_proto_line_no = min(self.first_proto_line_no, node.decl.coord.line)
        self.last_proto_line_no = max(self.last_proto_line_no, node.decl.coord.line)

        name = node.decl.name
        if name == "main":
            # we don't want to prototype main
            return

        return_type = self._generator.visit(node.decl.type.type)

        params = []
        if node.decl.type.args:
            for param in node.decl.type.args.params:
                param_type = self._generator.visit(param.type)
                param_name = param.name if param.name else ""

                # handle function pointer parameters
                if isinstance(param.type, c_ast.PtrDecl) and isinstance(
                    param.type.type, c_ast.FuncDecl
                ):
                    func_ptr = self._generator.visit(param.type)
                    # parameter name back into the function ptr declaration
                    func_ptr = func_ptr.replace("(*)", f"(*{param_name})")
                    params.append(func_ptr)
                else:
                    # regular parameters
                    parameter = param_type
                    # special formatting for pointers
                    parameter += " " if param_name and not param_type.endswith("*") else ""
                    parameter += param_name
                    params.append(parameter)

        param_str = ", ".join(params) if len(params) != 0 else "void"

        # nice formatting
        proto = f"{return_type} " if not return_type.endswith("*") else return_type
        proto += f"{name}({param_str});\n"

        self.protos.append(proto)
        self.protos_map[name] = proto


def _visit_file(filepath: str) -> HeaderVisitor | SourceVisitor:
    """Parse the file and extracts the prototypes.

    Args:
        filepath: the path to the file

    Returns:
        the visitor object
    """
    v = HeaderVisitor() if filepath.endswith(".h") else SourceVisitor()

    # parse the preprocessed file and fake headers
    ast = parse_file(filepath, use_cpp=True, cpp_args="-I" + pycparser_fake_libc.directory)
    v.visit(ast)

    return v


def _merge_prototypes(header_visitor: HeaderVisitor, src_visitor: SourceVisitor) -> list[str]:
    """Merge the existing prototypes and the new ones.

    Args:
        header_visitor: the visitor object of the header file
        src_visitor: the visitor object of the source file

    Returns:
        the prototypes that should be written to the header.
    """
    # we try to keep the order to avoid messing up
    # visually
    final_protos = []
    visited = set()

    old_protos = header_visitor.protos_map
    new_protos = src_visitor.protos_map

    for old_proto_name in old_protos.keys():
        # start by adding all protos where names match
        if old_proto_name in new_protos:
            final_protos.append(new_protos[old_proto_name])
            visited.add(old_proto_name)

    # add new protos
    for new_proto_name, new_proto in new_protos.items():
        if new_proto_name not in visited:
            final_protos.append(new_proto)

    return final_protos


def _validate_header_structure(
    source_filepath: str, header_filepath: str, existing_prototypes: list[str]
) -> None:
    with open(header_filepath) as f:
        header = f.read().strip()

    if not header or len(existing_prototypes) == 0:
        # The header file is empty or there are no existing prototypes
        # Generate a new header structure
        _generate_header(
            source_filepath=source_filepath, header_filepath=header_filepath, prototypes=[]
        )


def _generate_header(source_filepath: str, header_filepath: str, prototypes: list[str]) -> None:
    """Generate a header file from the prototypes.

    Args:
        source_filepath: the source filepath
        header_filepath: the destination filepath
        prototypes: the function prototypes
    """
    # we use a classic header name here
    header_name = os.path.basename(source_filepath).replace(".c", "_H").upper()
    header = f"#ifndef {header_name}\n#define {header_name}\n\n"

    if prototypes:
        header += "".join(prototypes)
        header += "\n"  # Add a newline after the prototypes

    header += f"\n#endif // {header_name}\n"  # Add newlines before and after the endif

    with open(header_filepath, "w") as f:
        f.write(header)


def _update_header(
    header_filepath: str, header_visitor: HeaderVisitor, src_visitor: SourceVisitor
) -> None:
    """Updates a header file with the changed prototypes."""
    protos = _merge_prototypes(header_visitor, src_visitor)

    with open(header_filepath, "r+") as f:
        content = f.readlines()

        # insert new prototypes after the #define
        insert_position = (
            next((i for i, line in enumerate(content) if line.strip().startswith("#define")), 0) + 1
        )

        # add newline after #define if it doesn't exist
        if insert_position > 0 and not content[insert_position - 1].strip() == "":
            content.insert(insert_position, "\n")
            insert_position += 1

        # remove existing protos
        start_remove = insert_position
        end_remove = next(
            (
                i
                for i, line in enumerate(content[insert_position:], start=insert_position)
                if line.strip().startswith("#endif")
            ),
            len(content),
        )
        del content[start_remove:end_remove]

        # insert new prototypes
        content[insert_position:insert_position] = protos

        # newline before #endif
        if content[insert_position + len(protos)].strip().startswith("#endif"):
            content.insert(insert_position + len(protos), "\n")

        f.seek(0)
        f.writelines(content)
        f.truncate()


def generate_prototypes(
    source_filepath: str, header_filepath: str | None = None, overwrite: bool = True
) -> list[str] | None:
    """Generate function prototypes from a source file.

    Args:
        overwrite: whether to overwrite the header file
        source_filepath: the source file
        header_filepath: the file to dump the prototypes to

    Returns:
        the prototypes
    """
    source_visitor = _visit_file(filepath=source_filepath)
    protos = source_visitor.protos

    if header_filepath:
        # check if header already exists, if so
        # add the protos to the file without overwriting anything
        if os.path.exists(header_filepath):
            if not overwrite:
                raise ValueError("A header file already exists at provided location.")

            header_visitor = _visit_file(header_filepath)

            # check if the header is correct
            # else create a correct structure
            _validate_header_structure(
                header_filepath=header_filepath,
                source_filepath=source_filepath,
                existing_prototypes=header_visitor.protos,
            )

            _update_header(
                header_filepath=header_filepath,
                header_visitor=header_visitor,
                src_visitor=source_visitor,
            )

        else:
            _generate_header(source_filepath, header_filepath, protos)

    return protos


def cli_generate():
    """CLI generation function."""
    parser = argparse.ArgumentParser(description="Generate C prototypes from source files.")
    parser.add_argument("source", help="Path to the source C file.")
    parser.add_argument("--header", help="Path to the header file.", required=False)
    parser.add_argument("--overwrite", help="Overwrite existing header file.", required=False)
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    generate_prototypes(
        source_filepath=args.source, header_filepath=args.header, overwrite=args.overwrite
    )
