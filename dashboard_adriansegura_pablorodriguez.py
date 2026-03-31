from pathlib import Path

import altair as alt
import pandas as pd
import streamlit as st


INPUT_FILE = Path("simpsons_episodes_clean.csv")

df = pd.read_csv(INPUT_FILE)


################################ CHARTS ################################
def correlation_chart():
    corr = df["imdb_rating"].corr(df["us_viewers_in_millions"])

    chart = alt.Chart(df).mark_circle(size=80, opacity=0.55).encode(
        x=alt.X(
            "imdb_rating:Q",
            title="IMDb rating",
            scale=alt.Scale(domain=[4, 10]),
        ),
        y=alt.Y(
            "us_viewers_in_millions:Q",
            title="US viewers (millions)",
            scale=alt.Scale(domainMin=0),
        ),
        tooltip=[
            alt.Tooltip("title:N", title="Episode"),
            alt.Tooltip("imdb_rating:Q", title="IMDb rating", format=".1f"),
            alt.Tooltip("us_viewers_in_millions:Q", title="Viewers", format=".2f"),
        ],
    )

    trend = alt.Chart(df).transform_regression(
        "imdb_rating", "us_viewers_in_millions"
    ).mark_line(size=3, clip=True, color="red").encode(
        x=alt.X("imdb_rating:Q", scale=alt.Scale(domain=[4, 10])),
        y=alt.Y("us_viewers_in_millions:Q", scale=alt.Scale(domainMin=0)),
    )

    corr_text = alt.Chart(
        pd.DataFrame({"x": [4.5], "y": [32.5], "label": [f"Corr = {corr:.3f}"]})
    ).mark_text(
        align="left",
        baseline="top",
        fontSize=14,
        fontWeight="bold",
    ).encode(
        x="x:Q",
        y="y:Q",
        text="label:N",
    )

    takeaway_text = alt.Chart(
        pd.DataFrame(
            {
                "x": [4.25],
                "y": [29.8],
                "label": ["Episodes with higher ratings tend to attract more viewers."],
            }
        )
    ).mark_text(
        align="left",
        baseline="top",
        fontSize=12,
        color="#555",
    ).encode(
        x="x:Q",
        y="y:Q",
        text="label:N",
    )

    return (chart + trend + corr_text + takeaway_text).properties(
        title="Correlation between ratings and viewers",
        width=650,
        height=400,
    ).configure_title(fontSize=16, anchor="middle")


def weekday_viewers_boxplot():
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return alt.Chart(df).mark_boxplot(size=36).encode(
        x=alt.X(
            "weekday:N",
            sort=weekday_order,
            title=None,
            axis=alt.Axis(labelAngle=0),
        ),
        y=alt.Y("us_viewers_in_millions:Q", title="US viewers (millions)"),
    ).properties(
        width=550,
        height=150,
    )



def weekday_numepisodes_bar():
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    return alt.Chart(df).mark_bar().encode(
        x=alt.X(
            "weekday:N",
            sort=weekday_order,
            title="Weekday aired",
            axis=alt.Axis(labelAngle=0),
        ),
        y=alt.Y("count():Q", title="Number of episodes"),
        tooltip=[
            alt.Tooltip("weekday:N", title="Weekday"),
            alt.Tooltip("count():Q", title="Episodes"),
        ],
    ).properties(
        width=550,
        height=150,
    )


def weekday_patterns_panel():
    return alt.vconcat(
        weekday_viewers_boxplot(),
        weekday_numepisodes_bar(),
        spacing=26,
    ).properties(
        title="Broadcast patterns by weekday",
    ).configure_title(fontSize=16, anchor="middle")


def viewers_heatmap():
    base = alt.Chart(df).encode(
        x=alt.X(
            "season:O",
            title="Season",
            axis=alt.Axis(labelAngle=0, orient="top"),
        ),
        y=alt.Y(
            "number_in_season:O",
            title="Episode number",
            sort="ascending",
        ),
    )

    heatmap = base.mark_rect(cornerRadius=4).encode(
        color=alt.Color(
            "us_viewers_in_millions:Q",
            title="US viewers (millions)",
            scale=alt.Scale(scheme="cividis"),
        ),
        tooltip=[
            alt.Tooltip("season:O", title="Season"),
            alt.Tooltip("number_in_season:O", title="Episode"),
            alt.Tooltip("title:N", title="Title"),
            alt.Tooltip("us_viewers_in_millions:Q", title="US viewers", format=".1f"),
        ],
    )

    return heatmap.properties(
        width=650,
        height=360,
        title="US viewers per episode across seasons",
    ).configure_title(fontSize=16, anchor="middle")


def ratings_heatmap():
    base = alt.Chart(df).encode(
        x=alt.X(
            "season:O",
            title="Season",
            axis=alt.Axis(labelAngle=0, orient="top"),
        ),
        y=alt.Y(
            "number_in_season:O",
            title="Episode number",
            sort="ascending",
        ),
    )

    heatmap = base.mark_rect(cornerRadius=6).encode(
        color=alt.Color(
            "rating_group:N",
            title="Rating",
            scale=alt.Scale(
                domain=["< 5", "5.0 - 5.9", "6.0 - 6.9", "7.0 - 7.9", "8.0 - 8.9", "9.0 - 10.0"],
                range=["#780000", "#D73939", "#d47336", "#f9ec5f", "#3dbd3d", "#005800"],
            ),
        ),
        tooltip=[
            alt.Tooltip("season:O", title="Season"),
            alt.Tooltip("number_in_season:O", title="Episode"),
            alt.Tooltip("title:N", title="Title"),
            alt.Tooltip("imdb_rating:Q", title="IMDb rating", format=".1f"),
        ],
    )

    return heatmap.properties(
        width=650,
        height=360,
        title="IMDb episode ratings by season",
    ).configure_title(fontSize=16, anchor="middle")


def viewers_boxplot():
    mean_viewers = df["us_viewers_in_millions"].mean()
    season_order = sorted(df["season"].astype(int).unique())
    last_season = season_order[-1]
    last_season_mean = df.loc[
        df["season"].astype(int) == last_season, "us_viewers_in_millions"
    ].mean()

    chart_box = alt.Chart(df).mark_boxplot(size=18, opacity=0.65).encode(
        x=alt.X(
            "season:O",
            title="Season number",
            sort=season_order,
            axis=alt.Axis(labelAngle=0),
        ),
        y=alt.Y(
            "us_viewers_in_millions:Q",
            title="US viewers (millions)",
            scale=alt.Scale(zero=False),
        ),
    )

    chart_line = alt.Chart(df).mark_line(
        point=alt.OverlayMarkDef(color="#1f3b5c"),
        color="#1f3b5c",
        strokeWidth=2,
    ).encode(
        x=alt.X("season:O", sort=season_order),
        y=alt.Y("mean(us_viewers_in_millions):Q"),
    )

    mean_rule = alt.Chart(pd.DataFrame({"y": [mean_viewers]})).mark_rule(
        color="firebrick",
        strokeDash=[6, 4],
        strokeWidth=2,
    ).encode(y="y:Q")

    labels = alt.Chart(
        pd.DataFrame(
            {
                "season": [last_season, last_season],
                "y": [last_season_mean, mean_viewers],
                "label": ["Season average", f"Global mean ({mean_viewers:.1f})"],
                "color": ["#1f3b5c", "firebrick"],
            }
        )
    ).mark_text(
        align="left",
        dx=20,
        fontSize=12,
        fontWeight="bold",
    ).encode(
        x=alt.X("season:O", sort=season_order),
        y="y:Q",
        text="label:N",
        color=alt.Color("color:N", scale=None),
    )

    return (chart_box + chart_line + mean_rule + labels).properties(
        title="Distribution of viewers by season",
        width=650,
        height=350,
    ).configure_title(fontSize=16, anchor="middle")


def ratings_boxplot():
    mean_rating = df["imdb_rating"].mean()
    season_order = sorted(df["season"].astype(int).unique())
    last_season = season_order[-1]
    last_season_mean = df.loc[
        df["season"].astype(int) == last_season, "imdb_rating"
    ].mean()

    chart_box = alt.Chart(df).mark_boxplot(size=18, opacity=0.65).encode(
        x=alt.X(
            "season:O",
            title="Season number",
            sort=season_order,
            axis=alt.Axis(labelAngle=0),
        ),
        y=alt.Y(
            "imdb_rating:Q",
            title="IMDb rating",
            scale=alt.Scale(zero=False),
        ),
    )

    chart_line = alt.Chart(df).mark_line(
        point=alt.OverlayMarkDef(filled=True, color="#1f3b5c"),
        color="#1f3b5c",
        strokeWidth=2,
    ).encode(
        x=alt.X("season:O", sort=season_order),
        y=alt.Y("mean(imdb_rating):Q"),
    )

    mean_rule = alt.Chart(pd.DataFrame({"y": [mean_rating]})).mark_rule(
        color="firebrick",
        strokeDash=[6, 4],
        strokeWidth=2,
    ).encode(y="y:Q")

    labels = alt.Chart(
        pd.DataFrame(
            {
                "season": [last_season, last_season],
                "y": [last_season_mean, mean_rating],
                "label": ["Season average", f"Global mean ({mean_rating:.1f})"],
                "color": ["#163a5f", "firebrick"],
            }
        )
    ).mark_text(
        align="left",
        dx=20,
        fontSize=12,
        fontWeight="bold",
    ).encode(
        x=alt.X("season:O", sort=season_order),
        y="y:Q",
        text="label:N",
        color=alt.Color("color:N", scale=None),
    )

    return (chart_box + chart_line + mean_rule + labels).properties(
        title="Distribution of IMDb ratings by season",
        width=650,
        height=350,
    ).configure_title(fontSize=16, anchor="middle")



################################ STREAMLIT CONFIG ################################
def render_chart(chart):
    _, center, _ = st.columns([0.005, 0.99, 0.005])
    with center:
        st.altair_chart(chart, width="content")


def boxed_container(*, key=None, border=True):
    try:
        return st.container(border=border, key=key)
    except TypeError:
        try:
            return st.container(border=border)
        except TypeError:
            return st.container()


def main():
    st.set_page_config(
        page_title="The decline of The Simpsons",
        layout="wide",
    )

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 1rem;
        }
        .st-key-heatmaps-row {
            margin-top: -1.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 0.35rem;'></div>", unsafe_allow_html=True)
    st.subheader("The decline of The Simpsons")
    st.markdown("<div style='height: 0.15rem;'></div>", unsafe_allow_html=True)


    # Viewers and ratings boxplots
    top_left, top_right = st.columns(2, gap="large")
    with top_left:
        render_chart(viewers_boxplot())
    with top_right:
        render_chart(ratings_boxplot())

    # Viewers and ratings heatmaps
    with boxed_container(key="heatmaps-row", border=False):
        middle_left, middle_right = st.columns(2, gap="large")
        with middle_left:
            render_chart(viewers_heatmap())
        with middle_right:
            render_chart(ratings_heatmap())

    # Weekday vs viewers and correlation charts
    bottom_left, bottom_right = st.columns(2, gap="large")
    with bottom_left:
        st.altair_chart(weekday_patterns_panel(), width="content")
    with bottom_right:
        render_chart(correlation_chart())

    # About section
    with st.expander("About"):
        st.write("Data Visualization MDS - First practical work")
        st.write("Authors: Adrian Segura and Pablo Rodriguez")


if __name__ == "__main__":
    main()
