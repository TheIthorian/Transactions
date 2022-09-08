import { Button, Card, Divider } from 'antd';
import { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';

import { ReloadOutlined } from '@ant-design/icons';

import Toolbar from 'components/toolbar';
import { getBreakdown } from './data';
import { LABELS } from './i18n';

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
    const [filter, setFilter] = useState(null);
    const [reload, setReload] = useState(false);

    useEffect(() => {
        getBreakdown(filter)
            .then(res => setData(res))
            .then(setLoaded(true));
    }, [filter, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    return (
        <Card loading={!loaded} style={{ marginTop: 10, maxWidth: '50vw' }}>
            <Toolbar title={LABELS.breakdownTitle}>
                <Button onClick={handleReload}>
                    <ReloadOutlined />
                </Button>
            </Toolbar>
            <Divider style={{ margin: '0 0 10px' }} />
            {loaded && data ? <Doughnut data={data} width='400' height='400'></Doughnut> : ''}
        </Card>
    );
}
