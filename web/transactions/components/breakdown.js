import { Card } from 'antd';
import { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import { getBreakdown } from './data';

import {
    Chart,
    ArcElement,
    LineElement,
    BarElement,
    PointElement,
    BarController,
    BubbleController,
    DoughnutController,
    LineController,
    PieController,
    PolarAreaController,
    RadarController,
    ScatterController,
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    RadialLinearScale,
    TimeScale,
    TimeSeriesScale,
    Decimation,
    Filler,
    Legend,
    Title,
    Tooltip,
    SubTitle,
} from 'chart.js';

Chart.register(
    ArcElement,
    LineElement,
    BarElement,
    PointElement,
    BarController,
    BubbleController,
    DoughnutController,
    LineController,
    PieController,
    PolarAreaController,
    RadarController,
    ScatterController,
    CategoryScale,
    LinearScale,
    LogarithmicScale,
    RadialLinearScale,
    TimeScale,
    TimeSeriesScale,
    Decimation,
    Filler,
    Legend,
    Title,
    Tooltip,
    SubTitle
);

export default function Breakdown() {
    const [loaded, setLoaded] = useState(false);
    const [data, setData] = useState(null);

    useEffect(() => {
        getBreakdown()
            .then(res => setData(res))
            .then(setLoaded(true));
    }, []);

    return (
        <Card loading={!loaded} style={{ margin: 10 }}>
            <span>Breakdown</span>
            {loaded && data ? <Doughnut data={data} width='400' height='400'></Doughnut> : ''}
        </Card>
    );
}
