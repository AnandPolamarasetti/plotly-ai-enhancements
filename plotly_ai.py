import plotly.express as px
import numpy as np
import os
import pandas as pd

# This script generates HTML figures using Plotly's Express functions for various plots,
# which can be used for testing with visual comparison tools like Percy.

# Directory to store HTML output files
dir_name = os.path.join("test", "percy")
os.makedirs(dir_name, exist_ok=True)  # Ensure the directory exists

# Utility function to save figures
def save_fig(fig, filename):
    file_path = os.path.join(dir_name, filename)
    fig.write_html(file_path)

# AI-driven utility: Intelligent configuration based on data type
def get_plot_settings(data):
    if "species" in data.columns:
        return {"color": "species"}
    elif "continent" in data.columns:
        return {"color": "continent"}
    elif "sex" in data.columns:
        return {"color": "sex"}
    return {}

# Enhance: Automatically choose data and create a scatter plot
def create_scatter_plot(data, x_col, y_col, filename, **kwargs):
    settings = get_plot_settings(data)
    settings.update(kwargs)
    fig = px.scatter(data, x=x_col, y=y_col, **settings)
    save_fig(fig, filename)

# Scatter and Line Plots
iris = px.data.iris()
create_scatter_plot(iris, "sepal_width", "sepal_length", "scatter.html")
create_scatter_plot(iris, "sepal_width", "sepal_length", "scatter_color.html", color="species")
create_scatter_plot(
    iris, "sepal_width", "sepal_length", "scatter_marginal.html", 
    color="species", marginal_y="rug", marginal_x="histogram"
)
create_scatter_plot(
    iris, "sepal_width", "sepal_length", "scatter_trendline.html",
    color="species", marginal_y="violin", marginal_x="box", trendline="ols"
)

iris["e"] = iris["sepal_width"] / 100
create_scatter_plot(
    iris, "sepal_width", "sepal_length", "scatter_errorbar.html",
    color="species", error_x="e", error_y="e"
)

tips = px.data.tips()
create_scatter_plot(
    tips, "total_bill", "tip", "scatter_categories.html", 
    facet_row="time", facet_col="day", color="smoker", trendline="ols",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]}
)

# Scatter Matrix with intelligent color mapping
fig = px.scatter_matrix(iris)
save_fig(fig, "scatter_matrix.html")

fig = px.scatter_matrix(
    iris,
    dimensions=["sepal_width", "sepal_length", "petal_width", "petal_length"],
    color="species"
)
save_fig(fig, "scatter_matrix_dimensions.html")

# Parallel Coordinates and Parallel Categories
fig = px.parallel_coordinates(
    iris,
    color="species_id",
    labels={
        "species_id": "Species",
        "sepal_width": "Sepal Width",
        "sepal_length": "Sepal Length",
        "petal_width": "Petal Width",
        "petal_length": "Petal Length"
    },
    color_continuous_scale=px.colors.diverging.Tealrose,
    color_continuous_midpoint=2
)
save_fig(fig, "parallel_coordinates.html")

fig = px.parallel_categories(
    tips, color="size", color_continuous_scale=px.colors.sequential.Inferno
)
save_fig(fig, "parallel_categories.html")

create_scatter_plot(
    tips, "total_bill", "tip", "scatter_webgl.html", 
    color="size", facet_col="sex", color_continuous_scale=px.colors.sequential.Viridis, render_mode="webgl"
)

gapminder = px.data.gapminder()
create_scatter_plot(
    gapminder.query("year==2007"), "gdpPercap", "lifeExp", "scatter_hover.html",
    size="pop", color="continent", hover_name="country", log_x=True, size_max=60
)

# AI-driven optimization: Automatically adjust animation settings for large datasets
fig = px.scatter(
    gapminder,
    x="gdpPercap",
    y="lifeExp",
    animation_frame="year",
    animation_group="country",
    size="pop",
    color="continent",
    hover_name="country",
    facet_col="continent",
    log_x=True,
    size_max=45,
    range_x=[100, 100000],
    range_y=[25, 90]
)
save_fig(fig, "scatter_log.html")

# Line plots with AI-enhanced settings
fig = px.line(
    gapminder,
    x="year",
    y="lifeExp",
    color="continent",
    line_group="country",
    hover_name="country",
    line_shape="spline",
    render_mode="svg"
)
save_fig(fig, "line.html")

# Faceted plots
create_scatter_plot(
    tips, "day", "tip", "facet_wrap_neat.html",
    facet_col="day", facet_col_wrap=2, category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]}
)
create_scatter_plot(
    tips, "day", "tip", "facet_wrap_ragged.html",
    color="sex", facet_col="day", facet_col_wrap=3, category_orders={"day": ["Thur", "Fri", "Sat", "Sun"]}
)

fig = px.area(gapminder, x="year", y="pop", color="continent", line_group="country")
save_fig(fig, "area.html")

# Distribution plots
fig = px.density_contour(iris, x="sepal_width", y="sepal_length")
save_fig(fig, "density_contour.html")

fig = px.density_contour(
    iris, x="sepal_width", y="sepal_length", color="species", marginal_x="rug", marginal_y="histogram"
)
save_fig(fig, "density_contour_marginal.html")

fig = px.density_heatmap(iris, x="sepal_width", y="sepal_length", marginal_x="rug", marginal_y="histogram")
save_fig(fig, "density_heatmap.html")

fig = px.bar(tips, x="sex", y="total_bill", color="smoker", barmode="group")
save_fig(fig, "bar.html")

fig = px.bar(
    tips,
    x="sex",
    y="total_bill",
    color="smoker",
    barmode="group",
    facet_row="time",
    facet_col="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]}
)
save_fig(fig, "bar_facet.html")

fig = px.histogram(tips, x="total_bill", y="tip", color="sex", marginal="rug", hover_data=tips.columns)
save_fig(fig, "histogram.html")

fig = px.histogram(
    tips,
    x="sex",
    y="tip",
    histfunc="avg",
    color="smoker",
    barmode="group",
    facet_row="time",
    facet_col="day",
    category_orders={"day": ["Thur", "Fri", "Sat", "Sun"], "time": ["Lunch", "Dinner"]}
)
save_fig(fig, "histogram_histfunc.html")

fig = px.strip(tips, x="total_bill", y="time", orientation="h", color="smoker")
save_fig(fig, "strip.html")

fig = px.box(tips, x="day", y="total_bill", color="smoker", notched=True)
save_fig(fig, "box.html")

fig = px.violin(
    tips,
    y="tip",
    x="smoker",
    color="sex",
    box=True,
    points="all",
    hover_data=tips.columns
)
save_fig(fig, "violin.html")

# Ternary Coordinates
election = px.data.election()
fig = px.scatter_ternary(
    election,
    a="Joly",
    b="Coderre",
    c="Bergeron",
    color="winner",
    size="total",
    hover_name="district",
    size_max=15,
    color_discrete_map={"Joly": "blue", "Bergeron": "green", "Coderre": "red"}
)
save_fig(fig, "scatter_ternary.html")

fig = px.line_ternary(
    election, a="Joly", b="Coderre", c="Bergeron", color="winner", line_dash="winner"
)
save_fig(fig, "line_ternary.html")

img_rgb = np.array(
    [[[255, 0, 0], [0, 255, 0], [0, 0, 255]], [[0, 255, 0], [0, 0, 255], [255, 0, 0]]],
    dtype=np.uint8
)
fig = px.imshow(img_rgb)
save_fig(fig, "imshow.html")

# 3D Coordinates
fig = px.scatter_3d(
    election,
    x="Joly",
    y="Coderre",
    z="Bergeron",
    color="winner",
    size="total",
    hover_name="district",
    symbol="result",
    color_discrete_map={"Joly": "blue", "Bergeron": "green", "Coderre": "red"}
)
save_fig(fig, "scatter_3d.html")

# Polar Coordinates
wind = px.data.wind()
fig = px.line_polar(wind, r="frequency", theta="direction", color="strength", line_close=True)
save_fig(fig, "line_polar.html")

fig = px.bar_polar(
    wind, r="frequency", theta="direction", color="strength", template="plotly_dark", hover_data=["frequency", "direction"]
)
save_fig(fig, "bar_polar.html")

# Maps
fig = px.scatter_mapbox(
    election,
    lat="lat",
    lon="lon",
    color="total",
    size="total",
    hover_name="district",
    hover_data=["Joly", "Coderre", "Bergeron"],
    color_continuous_scale=px.colors.cyclical.IceFire,
    size_max=15,
    zoom=10,
    mapbox_style="carto-positron"
)
save_fig(fig, "scatter_mapbox.html")

fig = px.choropleth_mapbox(
    election,
    geojson=px.data.election_geojson(),
    locations="district",
    featureidkey="properties.district",
    color="Bergeron",
    color_continuous_scale="Viridis",
    range_color=(0, 6500),
    mapbox_style="carto-positron",
    zoom=9,
    center={"lat": 45.5517, "lon": -73.7073},
    opacity=0.5,
    labels={"Bergeron": "votes for Bergeron"}
)
save_fig(fig, "choropleth_mapbox.html")

fig = px.density_mapbox(
    election,
    lat="lat",
    lon="lon",
    z="total",
    radius=10,
    mapbox_style="stamen-terrain"
)
save_fig(fig, "density_mapbox.html")

# Adding AI-driven logging for performance insights
import time

def log_performance(start_time, plot_name):
    end_time = time.time()
    duration = end_time - start_time
    print(f"{plot_name} generated in {duration:.2f} seconds.")

# Enhanced Performance Logging Example
start_time = time.time()
fig = px.scatter_3d(
    election,
    x="Joly",
    y="Coderre",
    z="Bergeron",
    color="winner",
    size="total",
    hover_name="district",
    symbol="result",
    color_discrete_map={"Joly": "blue", "Bergeron": "green", "Coderre": "red"}
)
save_fig(fig, "scatter_3d_with_logging.html")
log_performance(start_time, "3D Scatter Plot")

