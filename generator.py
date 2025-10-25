"""
1. read data from csv
2. generate json files for charts
3. save json files to data directory
4. generate astro site for each place, plots.astro with correct paths to json files


"""

import pandas as pd

import json
from plotly.utils import PlotlyJSONEncoder
import ladybug_charts
from ladybug.analysisperiod import AnalysisPeriod
from ladybug.header import Header
from ladybug.datacollection import HourlyContinuousCollection
from ladybug.dt import DateTime
from ladybug.datatype.temperature import Temperature
from ladybug.datatype.fraction import HumidityRatio
from ladybug.datatype.speed import WindSpeed
from ladybug.datatype.angle import WindDirection
from ladybug.windrose import WindRose
from ladybug.psychchart import PsychrometricChart
from ladybug.hourlyplot import HourlyPlot


full_meta_stations ={
    'STATION_NAME': [
        'Adelboden',
        'Aigle',
        'Altdorf',
        'Basel / Binningen',
        'Bern / Zollikofen',
        'Buchs / Aarau',
        'Bullet / La Frétaz',
        'Chur',
        'Col du Grand St-Bernard',
        'Davos',
        'Disentis',
        'Engelberg',
        'Genève / Cointrin',
        'Glarus',
        'Güttingen',
        'Interlaken',
        'La Chaux-de-Fonds',
        'Locarno / Monti',
        'Lugano',
        'Luzern',
        'Magadino / Cadenazzo',
        'Montana',
        'Neuchâtel',
        'Payerne',
        'Piotta',
        'Poschiavo / Robbia',
        'Pully',
        'Rünenberg',
        'S. Bernardino',
        'Samedan',
        'Schaffhausen',
        'Scuol',
        'Sion',
        'St. Gallen',
        'Ulrichen',
        'Vaduz',
        'Wynau',
        'Zermatt',
        'Zürich / Affoltern',
        'Zürich / Fluntern',
        'Zürich / Kloten'
    ],
    'NAT_ABBR': [
        'ABO',
        'AIG',
        'ALT',
        'BAS',
        'BER',
        'BUS',
        'FRE',
        'CHU',
        'GSB',
        'DAV',
        'DIS',
        'ENG',
        'GVE',
        'GLA',
        'GUT',
        'INT',
        'CDF',
        'OTL',
        'LUG',
        'LUZ',
        'MAG',
        'MVE',
        'NEU',
        'PAY',
        'PIO',
        'ROB',
        'PUY',
        'RUE',
        'SBE',
        'SAM',
        'SHA',
        'SCU',
        'SIO',
        'STG',
        'ULR',
        'VAD',
        'WYN',
        'ZER',
        'REH',
        'SMA',
        'KLO'
    ],
    'LATITUDE': [
        46.492,
        46.327,
        46.887,
        47.541,
        46.991,
        47.384,
        46.841,
        46.87,
        45.869,
        46.813,
        46.707,
        46.822,
        46.248,
        47.035,
        47.602,
        46.672,
        47.083,
        46.173,
        46.004,
        47.036,
        46.16,
        46.299,
        47.0,
        46.812,
        46.515,
        46.347,
        46.512,
        47.435,
        46.464,
        46.526,
        47.69,
        46.793,
        46.219,
        47.425,
        46.505,
        47.127,
        47.255,
        46.029,
        47.428,
        47.378,
        47.48
    ],
    'LONGITUDE': [
        7.5604,
        6.9244,
        8.6218,
        7.5836,
        7.464,
        8.0794,
        6.5763,
        9.5305,
        7.1708,
        9.8435,
        8.8535,
        8.4105,
        6.1277,
        9.0669,
        9.2794,
        7.8701,
        6.7923,
        8.7874,
        8.9603,
        8.301,
        8.9337,
        7.4608,
        6.9533,
        6.9424,
        8.6881,
        10.0611,
        6.6674,
        7.8793,
        9.1846,
        9.8795,
        8.6201,
        10.2832,
        7.3302,
        9.3985,
        8.3081,
        9.5175,
        7.7874,
        7.7531,
        8.5179,
        8.5657,
        8.5359
    ],
    'XCOORD': [
        609350,
        560401,
        690174,
        610911,
        601930,
        648389,
        534221,
        759466,
        579200,
        783514,
        708189,
        674157,
        498905,
        723752,
        738420,
        633019,
        550919,
        704160,
        717874,
        665540,
        715480,
        601706,
        563087,
        562127,
        695888,
        801850,
        540811,
        633246,
        734112,
        787250,
        688698,
        817135,
        591630,
        747865,
        666740,
        757719,
        626400,
        624350,
        681428,
        685117,
        682710
    ],
    'YCOORD': [
        149001,
        130713,
        193558,
        265601,
        204410,
        248365,
        188081,
        193153,
        79720,
        187458,
        173789,
        186097,
        122632,
        210568,
        273960,
        169093,
        214861,
        114350,
        95884,
        209848,
        113162,
        127482,
        205560,
        184612,
        152261,
        136180,
        151514,
        253846,
        147296,
        155685,
        282796,
        186393,
        118575,
        254588,
        150760,
        221697,
        233850,
        97560,
        253546,
        248066,
        259339
    ],
    'ELEVATION': [
        1326.74,
        381.02,
        438.0,
        316.17,
        552.84,
        386.66,
        1205.43,
        556.0,
        2472.0,
        1594.16,
        1197.05,
        1035.66,
        410.88,
        516.62,
        440.02,
        577.34,
        1017.01,
        366.75,
        273.0,
        454.0,
        203.2,
        1427.0,
        485.0,
        490.0,
        990.0,
        1078.0,
        455.61,
        611.17,
        1638.7,
        1708.51,
        438.0,
        1303.93,
        482.0,
        775.66,
        1345.87,
        457.25,
        422.0,
        1638.35,
        443.53,
        555.95,
        426.26
    ],
    'SLUGS': [
        'adelboden',
        'aigle',
        'altdorf',
        'basel-binningen',
        'bern-zollikofen',
        'buchs-aarau',
        'bullet-la-fretaz',
        'chur',
        'col-du-grand-st-bernard',
        'davos',
        'disentis',
        'engelberg',
        'geneve-cointrin',
        'glarus',
        'guttingen',
        'interlaken',
        'la-chaux-de-fonds',
        'locarno-monti',
        'lugano',
        'luzern',
        'magadino-cadenazzo',
        'montana',
        'neuchatel',
        'payerne',
        'piotta',
        'poschiavo-robbia',
        'pully',
        'runenberg',
        's-bernardino',
        'samedan',
        'schaffhausen',
        'scuol',
        'sion',
        'st-gallen',
        'ulrichen',
        'vaduz',
        'wynau',
        'zermatt',
        'zurich-affoltern',
        'zurich-fluntern',
        'zurich-kloten'
    ]
}



def psych_charteric_plot(temp_data, rel_hum_data):
    analysis_period = AnalysisPeriod.from_start_end_datetime(
        DateTime(1, 1, 0, 0), DateTime(12, 31, 23, 0), 1
    )

    header_temperature = Header(Temperature(), "C", analysis_period, metadata=None)
    header_rel_hum = Header(HumidityRatio(), "%", analysis_period, metadata=None)

    data_temp = HourlyContinuousCollection(header_temperature, temp_data.tolist())
    data_rel_hum = HourlyContinuousCollection(header_rel_hum, rel_hum_data.tolist())

    lb_psy = PsychrometricChart(
        data_temp,
        data_rel_hum,
    )

    fig = lb_psy.plot()

    fig.update_layout(
        xaxis=dict(
            color="white",
        ),
        yaxis=dict(
            color="white",
        ),
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(4,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        template="simple_white",
    )
    return fig



def hourly_plot(temp_data):
    analysis_period = AnalysisPeriod.from_start_end_datetime(
        DateTime(1, 1, 0, 0), DateTime(12, 31, 23, 0), 1
    )

    header_temperature = Header(Temperature(), "C", analysis_period, metadata=None)
    header_rel_hum = Header(HumidityRatio(), "%", analysis_period, metadata=None)

    data_temp = HourlyContinuousCollection(header_temperature, temp_data.tolist())
    hp = HourlyPlot(data_temp)
    fig = hp.plot()
    fig.print_grid = False
    fig.update_layout(
        xaxis=dict(
            color="white",
        ),
        yaxis=dict(
            color="white",
        ),
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        template="simple_white",
    )
    return fig



def wind_plot(wind_avg, wind_direction):
    analysis_period = AnalysisPeriod.from_start_end_datetime(
        DateTime(1, 1, 0, 0), DateTime(12, 31, 23, 0), 1
    )
    header_wind = Header(WindSpeed(), "m/s", analysis_period, metadata=None)
    header_wind_direction = Header(
        WindDirection(), "degrees", analysis_period, metadata=None
    )

    data_wind = HourlyContinuousCollection(header_wind, wind_avg.tolist())
    data_wind_direction = HourlyContinuousCollection(
        header_wind_direction, wind_direction.tolist()
    )

    lb_wind_rose = WindRose(data_wind_direction, data_wind)
    fig = lb_wind_rose.plot()

    fig.update_layout(
        legend_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        polar=dict(
            bgcolor="rgba(0, 0, 0,0)",
            angularaxis=dict(
                linewidth=2,
                showline=True,
                linecolor="white",
            ),
        ),
    )
    return fig

class Template:
    def __init__(self, station_name, slug, short) -> None:
        self.STATION_NAME: str = station_name
        self.SLUG: str = slug
        self.NAT_ABBR: str = short

    def generate_template(self):
        return f"""---
import Header from "../components/Header.astro";
import Sidebar from "../components/Sidebar.astro";
import PlotlyChart from "../components/PlotlyChart.astro";
---
<!doctype html>
<html>
<Header title="{self.STATION_NAME}" />
<body>
    <div class="content">
    <Sidebar selectedItem="{self.SLUG}" />
    <nav class="main">
        <div class="container">
        <div class="back-nav-container">
            <a href="/" class="back-nav-button w-inline-block"
            ><img
                src="/assets/back.svg"
                loading="lazy"
                alt=""
                class="back-nav-img"
            />
            <div>Back</div></a
            >
        </div>
        <div class="content-container">
            <h1>{self.STATION_NAME}</h1>
            <section class="items-container">
            <h3>Psychometric</h3>
            <PlotlyChart dataPath="/data/{self.NAT_ABBR}/psych_chart.json" chartId="{self.NAT_ABBR}-psych" />
            <h3>Temperature</h3>
            <PlotlyChart dataPath="/data/{self.NAT_ABBR}/hourly_chart.json" chartId="{self.NAT_ABBR}-hourly"/>
            <h3>Wind</h3>
            <PlotlyChart dataPath="/data/{self.NAT_ABBR}/wind_chart.json" chartId="{self.NAT_ABBR}-wind"/>
            </section>
        </div>
        </div>
    </nav>
    </div>

</body>
</html>
        """

    def save_template(self, path):
        with open(path, "w", encoding="utf-8") as f:
            f.write(self.generate_template())

def create_astro_file(full_meta_stations):

    for id in range(0, len(full_meta_stations["NAT_ABBR"])):
        astro_file_path = f"src/pages/{full_meta_stations['SLUGS'][id]}.astro"
        data_folder = f"/data/{full_meta_stations['NAT_ABBR'][id]}"
        # <PlotlyChart dataPath="/data/anotherChart.json" chartId="lafsdjk"/>
        template = Template(
            full_meta_stations["STATION_NAME"][id],
            full_meta_stations["SLUGS"][id],
            full_meta_stations["NAT_ABBR"][id],
        )
        template.save_template(astro_file_path)


  
def create_json_plot_config(full_meta_stations):

    for short_name in full_meta_stations["NAT_ABBR"]:
        folder = f"public/data/{short_name}"
        csv_file_path = f"{folder}/{short_name}_2035_RCP85_DRY.csv"

        df_sma = pd.read_csv(csv_file_path)
        sma_2035_temp = df_sma["tre200h0"].values
        sma_2035_rel_hum = df_sma["ure200h0"].values
        wind_avg = df_sma["fkl010h0"].values
        wind_direction = df_sma["dkl010h0"].values

        fig_wind = wind_plot(wind_avg, wind_direction)
        with open(f"{folder}/wind_chart.json", "w") as f:
            f.write(json.dumps(fig_wind, cls=PlotlyJSONEncoder))

        fig_psych = psych_charteric_plot(sma_2035_temp, sma_2035_rel_hum)
        with open(f"{folder}/psych_chart.json", "w") as f:
            f.write(json.dumps(fig_psych, cls=PlotlyJSONEncoder))

        fig_hourly = hourly_plot(sma_2035_temp)
        with open(f"{folder}/hourly_chart.json", "w") as f:
            f.write(json.dumps(fig_hourly, cls=PlotlyJSONEncoder))




if __name__ == "__main__":
  create_json_plot_config(full_meta_stations)
  create_astro_file(full_meta_stations)
