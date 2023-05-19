from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel, Field

class AutoTraceParameters(BaseModel):
    # following https://github.com/autotrace/autotrace#usage
    background_color: str = Field(
        "FFFFFF", 
        alias="-background-color", 
        description=" <hexadecimal>;  the color of the background that should be ignored, for example FFFFFF; default is no background color."
    )
    centerline: str = Field(
        "-centerline",
        alias="-centerline",
        description="trace a character's centerline, rather than its outline."
    )
    charcode: str = Field(
        alias="-charcode", 
        description=" <unsigned>;  code of character to load from GF font file."
    )
    color_count: int = Field(
        0,
        alias="-color-count", 
        description=" <unsigned>;  number of colors a color bitmap is reduced to, it does not work on grayscale, allowed are 1..256; default is 0, that means no color reduction is done."
    )
    corner_always_threshold: int = Field(
        60,
        alias="-corner-always-threshold", 
        description=" <angle-in-degrees>;  if the angle at a pixel is less than this, it is considered a corner, even if it is within `corner-surround' pixels of another corner; default is 60."
    )
    corner_surround: int = Field(
        4,
        alias="-corner-surround", 
        description=" <unsigned>;  number of pixels on either side of a point to consider when determining if that point is a corner; default is 4."
    )
    corner_threshold: int = Field(
        100,
        alias="-corner-threshold", 
        description=" <angle-in-degrees>;  if a pixel, its predecessor(s), and its successor(s) meet at an angle smaller than this, it's a corner; default is 100."
    )
    despeckle_level: int = Field(
        0,
        alias="-despeckle-level",
        description="<unsigned>: 0..20; default is 0; no despeckling."
    )
    despeckle_tightness: float = Field(
        2.0,
        alias="-despeckle-tightness", 
        description=" <real>;  0.0..8.0; default is 2.0."
    )
    dpi: str = Field(
        alias="-dpi", 
        description=" <unsigned>;  The dots per inch value in the input image, affects scaling of mif output image"
    )
    error_threshold: float = Field(
        2.0,
        alias="-error-threshold", 
        description=" <real>;  subdivide fitted curves that are off by more pixels than this; default is 2.0."
    )
    filter_iterations: int = Field(
        4,
        alias="-filter-iterations",
        description=" <unsigned>;  smooth the curve this many times before fitting; default is 4."
    )
    input_format: str = Field(
        "svg",
        alias="-input-format",
        description="Available formats;  ppm, png, pbm, pnm, bmp, tga, pgm, gf."
    )
    help: str = Field(
        alias="-help",
        description="print this message."
    )
    line_reversion_threshold: float = Field(
        .01,
        alias="-line-reversion-threshold", 
        description=" <real>;  if a spline is closer to a straight line than this, weighted by the square of the curve length, keep it a straight line even if it is a list with curves; default is .01."
    )
    line_threshold: float = Field(
        1.0,
        alias="-line-threshold",
        description=" <real>;  if the spline is not more than this far away from the straight line defined by its endpoints, then output a straight line; default is 1."
    )
    list_output_formats: str = Field(
        alias="-list-output-formats",
        description="print a list of supported output formats to stderr."
    )
    list_input_formats: str = Field(
        alias="-list-input-formats",
        description="print a list of supported input formats to stderr."
    )
    log: str = Field(
        alias="-log", 
        description="write detailed progress reports to <input_name>.log."
    )
    noise_removal: float = Field(
        0.99,
        alias="-noise-removal",
        description=" <real>:;  0.0..1.0; default is 0.99."
    )
    output_file: str = Field(
        alias="-output-file",
        description=" <filename>;  write to <filename>"
    )
    output_format: str = Field(
        "svg",
        alias="-output-format",
        description="<format>: use format <format> for the output file. Available formats; rpl, tk, cfdg, xfig, plot, svg, plot-svg, gschem, gmfa, text, epd, tek, rib, sk, plot-tek, gmfb, pcl, txt, asy, plot-pcl, tex, gnuplot, cairo, dat, plot-hpgl, lwo, pcb, xml, dr2d, pov, dxf_14, eps, tfig, mp, meta, java1, hpgl, ai, cgm, pdf, latex2e, ps2ai, p2e, java2, pic, svm, plot-cgm, plot-ai, plt, noixml, vtk, tgif, idraw, fig, emf, plot-fig, kil, er, m, dxf, obj, ugs, pcbfill, mif, mma, java, gcode, c, dxf_s, ild, mpost, pcbi"
    )
    preserve_width: str = Field(
        alias="-preserve-width",
        description="preserve line width prior to thinning."
    )
    remove_adjacent_corners: str = Field(
        alias="-remove-adjacent-corners",
        description="remove corners that are adjacent."
    )
    tangent_surround: int = Field(
        3,
        alias="-tangent-surround", 
        description=" <unsigned>;  number of points on either side of a point to consider when computing the tangent at that point; default is 3."
    )
    version: str = Field(
        alias="-version",
        description="print the version number of this program."
    )
    width_weight_factor: float = Field(
        alias="-width-weight-factor", 
        description=" <real>;  weight factor for fitting the linewidth."
    )


app = FastAPI()



@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/autotrace/")
async def autotrace(the_parameters: AutoTraceParameters, file: UploadFile):
    return {"parameters": the_parameters, "filename": file.name}