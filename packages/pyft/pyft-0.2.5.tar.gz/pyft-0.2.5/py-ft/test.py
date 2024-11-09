
import pyft
import polars as pl

df=pyft.utils.read_extract_all("test.tbl", long=True, pandas=True)
print(df[["long_start", "long_end", "long_ref_start", "long_ref_end", "type"]])
chart = pyft.plot.extract_chart(df, max_fibers=50, ref=False)
chart.save("test.html")
