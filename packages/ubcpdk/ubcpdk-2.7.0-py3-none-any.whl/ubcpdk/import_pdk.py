import gdsfactory as gf

from ubcpdk.config import PATH

if __name__ == "__main__":
    print(
        gf.write_cells.get_import_gds_script(
            dirpath=PATH.gds / "EBeam", module="ubpdk.components"
        )
    )
    print(
        gf.write_cells.get_import_gds_script(
            dirpath="gds/EBeam_Beta", module="ubpdk.components"
        )
    )
