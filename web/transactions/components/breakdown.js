import { Button, Card, Divider, Select, Option } from 'antd';
import { useEffect, useState } from 'react';

import { ReloadOutlined } from '@ant-design/icons';

import Toolbar from 'components/toolbar';
import { getAllTags, getBreakdown } from './data';
import { LABELS } from './i18n';

import Chart from 'chart.js/auto';

// import {
//     Chart,
//     ArcElement,
//     LineElement,
//     BarElement,
//     PointElement,
//     BarController,
//     BubbleController,
//     DoughnutController,
//     LineController,
//     PieController,
//     PolarAreaController,
//     RadarController,
//     ScatterController,
//     CategoryScale,
//     LinearScale,
//     LogarithmicScale,
//     RadialLinearScale,
//     TimeScale,
//     TimeSeriesScale,
//     Decimation,
//     Filler,
//     Legend,
//     Title,
//     Tooltip,
//     SubTitle,
// } from 'chart.js';

// Chart.register(
//     ArcElement,
//     LineElement,
//     BarElement,
//     PointElement,
//     BarController,
//     BubbleController,
//     DoughnutController,
//     LineController,
//     PieController,
//     PolarAreaController,
//     RadarController,
//     ScatterController,
//     CategoryScale,
//     LinearScale,
//     LogarithmicScale,
//     RadialLinearScale,
//     TimeScale,
//     TimeSeriesScale,
//     Decimation,
//     Filler,
//     Legend,
//     Title,
//     Tooltip,
//     SubTitle
// );

function Canvas({ id, width, height, onload }) {
    useEffect(() => {
        onload(id);
    }, []);

    return <canvas {...{ id, width, height }}></canvas>;
}

export default function Breakdown() {
    const [loaded, setLoaded] = useState(true);
    const [data, setData] = useState(null);
    const [filter, setFilter] = useState(null);
    const [reload, setReload] = useState(false);
    const [allTags, setAllTags] = useState([]);

    useEffect(() => {
        getAllTags().then(res => {
            console.log(res);
            setAllTags(res);
        });
    }, [filter, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleChangeTagFilter(values) {
        setFilter(filter => ({ ...filter, tags: { l1: values } }));
    }

    if (!allTags.length && !data) {
        return <em>Loading...</em>;
    }

    return (
        <Card loading={!loaded} style={{ marginTop: 10, maxWidth: '50vw' }}>
            <Toolbar title={LABELS.breakdownTitle}>
                <Select
                    mode='multiple'
                    allowClear
                    style={{
                        width: '100%',
                    }}
                    placeholder='Filter by Tag'
                    onChange={handleChangeTagFilter}
                >
                    {allTags.length && allTags.map(tag => <Option key={tag}>{tag}</Option>)}
                </Select>
                <Button onClick={handleReload}>
                    <ReloadOutlined />
                </Button>
            </Toolbar>
            <Divider style={{ margin: '0 0 10px' }} />
            <Canvas
                id='breakdown-chart'
                width='400'
                height='400'
                onload={() => {
                    getBreakdown(filter)
                        .then(data => {
                            const ctx = document.querySelector('#breakdown-chart');
                            new Chart(ctx, data);
                        })
                        .then(() => setLoaded(true))
                        .catch();
                }}
            />
        </Card>
    );
}
