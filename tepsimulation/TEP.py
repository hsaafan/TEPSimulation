import flowsheet as F
import materials as M


def create_tep_F():
    mats = M.import_materials()
    fs = F.F(mats)
    streams = [
        F.MatStream("STREAM01", "A Feed"),
        F.MatStream("STREAM02", "D Feed"),
        F.MatStream("STREAM03", "E Feed"),
        F.MatStream("STREAM04", "C Feed"),
        F.MatStream("STREAM05", "Stripper Vapor"),
        F.MatStream("STREAM06", "Reactor Feed"),
        F.MatStream("STREAM07", "Reactor Product"),
        F.MatStream("STREAM08", "Compressor Outlet"),
        F.MatStream("STREAM09", "Gas Purge"),
        F.MatStream("STREAM10", "Separator Liquid"),
        F.MatStream("STREAM11", "Product Stream"),
        F.MatStream("STREAM12", "Reactor Cooling Water Inlet"),
        F.MatStream("STREAM13", "Condenser Cooling Water Inlet"),
        F.MatStream("STREAM14", "Reactor Cooling Water Outlet"),
        F.MatStream("STREAM15", "Condeser Cooling Water Outlet"),
        F.MatStream("STREAM16", "Stripper Steam Inlet"),
        F.MatStream("STREAM17", "Stripper Steam Outlet")
    ]
    for stream in streams:
        fs.add_stream(stream)
    unit_ops = [
        F.Reactor("REACTOR01", "Main Reactor"),
        F.Stripper("STRIPPER01", "Product Stripping Column"),
        F.VaporLiquidSeparator("VAPLIQSEP01", "Vapor Liquid Separator"),
        F.Compressor("COMPRESS01", "Recycle Stream Compressor"),
        F.Condenser("CONDENSER01", "Reactor Product Condenser")
    ]
    for uo in unit_ops:
        fs.add_unit_operation(uo)
    return
