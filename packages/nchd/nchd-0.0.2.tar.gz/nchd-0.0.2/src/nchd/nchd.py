"""
A command line utility to provide a better version of `ncdump -h` for netCDF files.
"""

from rich import print
from typing import Optional, Sequence
import argparse
import os
from netCDF4 import Dataset
from pathlib import Path


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="The netCDF file to display")
    args = parser.parse_args(argv)
    # print(args)

    file = args.file
    if not os.path.exists(file) or not os.path.isfile(file):
        print(f"File {file} does not exist.")
        return 1
    else:
        _read_and_display(file)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())


def _check_file_valid(file: str) -> bool:
    f_valid = os.path.exists(file) and os.path.isfile(file)
    if not f_valid:
        print(f"File {file} does not exist.")

    return f_valid


def _read_and_display(file: str) -> None:
    """
    Function that does all of the heavy lifting.
    """
    nc_fobj = _NcFileDisplay(file)
    print(nc_fobj)


class _NcFileDisplay:
    """
    Class to handle the display of the netCDF file.
    """

    def __init__(self, fname: str):
        self._fname = Path(fname)
        self._ds = Dataset(fname)

    def __str__(self):
        outstr = f"netcdf {self.fname} {{\n"

        outstr += "dimensions:\n"
        outstr += self.dimensions

        outstr += "\nvariables:\n"
        outstr += self.variables

        outstr += "\n\n// global attributes:\n"
        outstr += self.global_attributes

        outstr += "\n}\n"
        return outstr

    @property
    def fname(self) -> str:
        return self._fname.stem

    @property
    def dimensions(self) -> str:
        dims = self._ds.dimensions

        dim_str = "\n".join(
            [
                f"\t{dim} = {len(self._ds.dimensions[dim])} ;"
                if not self._ds.dimensions[dim].isunlimited()
                else f"\t{dim} = UNLIMITED ; // ({len(self._ds.dimensions[dim])} currently)"
                for dim in dims
            ]
        )
        return dim_str

    @property
    def variables(self) -> str:
        vars = self._ds.variables.keys()
        vars_str = "\n".join([f"{self._variable(var)}" for var in vars])
        return vars_str

    def _variable(self, varname) -> str:
        """
        pprints a single variable
        """
        var_str = f"\t{self._ds.variables[varname].dtype} {varname} {self._ds.variables[varname].dimensions} ;\n"
        # Now we need to print out the attributes
        attrs = self._ds.variables[varname].ncattrs()
        if len(attrs) > 0:
            var_str += "\n".join(
                [
                    f"\t\t{varname}:{attr} = {self._ds.variables[varname].getncattr(attr)} ;"
                    for attr in attrs
                ]
            )

        return var_str

    @property
    def global_attributes(self) -> str:
        attrs = self._ds.ncattrs()

        attr_str = "\n".join(
            [f"\t:{attr} = {self._ds.getncattr(attr)} ;" for attr in attrs]
        )

        return attr_str
