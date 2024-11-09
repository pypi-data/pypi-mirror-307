from IPython.core.magic import Magics, line_cell_magic, cell_magic, magics_class

from .utils import compile_run_c, handle_metadata


@magics_class
class GccMagic(Magics):
    @line_cell_magic
    def gcc(self, line, cell=None):
        """Compile and run C code using gcc."""
        if cell is None:
            with open(line)  as f:
                metadata_dict, code = handle_metadata(f.read())
                compile_run_c(code, metadata_dict)
            #return line
        else:
            metadata_dict, code = handle_metadata(cell)
            compile_run_c(code, metadata_dict)
            #return line, cell
