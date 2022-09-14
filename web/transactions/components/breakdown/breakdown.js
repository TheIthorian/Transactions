import { Button, Card, Divider, Select, Option, DatePicker } from 'antd';
import { useEffect, useState } from 'react';

import { ReloadOutlined } from '@ant-design/icons';

import Toolbar from 'components/toolbar';
import { getAllTags, getBreakdown } from './data';
import { LABELS } from 'components/i18n';

import Chart from 'chart.js/auto';
import { plugins } from 'chart.js';
import { makeHandleLegendClick } from './eventHandlers';

import { Doughnut } from 'react-chartjs-2';

// function Doughnut({ id, width, height, data }) {
//     useEffect(() => {
//         // onload(id);
//         try {
//             const ctx = document.querySelector('#breakdown-chart');
//             new Chart(ctx, data);
//         } catch {}
//     }, []);

//     return <canvas {...{ id, width, height }}></canvas>;
// }

export default function Breakdown() {
    const [loaded, setLoaded] = useState(true);
    const [data, setData] = useState(null);
    const [filter, setFilter] = useState({});
    const [reload, setReload] = useState(false);
    const [allTags, setAllTags] = useState([]);

    useEffect(() => {
        getAllTags().then(res => {
            console.log(res);
            setAllTags(res);
        });

        getBreakdown(filter)
            .then(setData)
            .then(() => setLoaded(true))
            .catch(console.log);
    }, [filter, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleChangeTagFilter(values) {
        setFilter(filter => ({ ...filter, tags: { l1: values } }));
    }

    function handleChangeDateFrom(value) {
        setFilter(filter => ({ ...filter, date_from: value?.format('YYYY-MM-DD') }));
    }

    function handleChangeDateTo(value) {
        setFilter(filter => ({ ...filter, date_to: value?.format('YYYY-MM-DD') }));
    }

    if (!allTags.length || !data || !loaded) {
        return <em>Loading...</em>;
    }

    return (
        <Card loading={!loaded} style={{ marginTop: 10, maxWidth: '50vw' }}>
            <Toolbar title={LABELS.breakdownTitle}>
                <DatePicker onChange={handleChangeDateFrom}>From</DatePicker>
                <DatePicker onChange={handleChangeDateTo}>To</DatePicker>
                <Select
                    mode='multiple'
                    allowClear
                    style={{
                        width: '100%',
                    }}
                    placeholder='Filter by Tag'
                    onChange={handleChangeTagFilter}
                >
                    {allTags.length &&
                        allTags.map(tag => (
                            <Option key={tag} value={tag}>
                                {tag}
                            </Option>
                        ))}
                </Select>
                <Button onClick={handleReload}>
                    <ReloadOutlined />
                </Button>
            </Toolbar>
            <Divider style={{ margin: '0 0 10px' }} />
            <Doughnut width='400' height='400' data={data.data} options={data.options} />
        </Card>
    );
}
