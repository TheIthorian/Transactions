import { Button, Card, Divider, Select, DatePicker, Skeleton, Space } from 'antd';
const { Option } = Select;

import { useEffect, useState } from 'react';

import { ReloadOutlined } from '@ant-design/icons';

import Toolbar from 'components/toolbar';
import { getAllTags, getBreakdown } from './data';
import { LABELS } from 'components/i18n';

import 'chart.js/auto';
import { Doughnut } from 'react-chartjs-2';

export default function Breakdown() {
    const [loaded, setLoaded] = useState(true);
    const [data, setData] = useState(null);
    const [filter, setFilter] = useState({
        tags: {
            l1: [
                'Appearance',
                'Bills',
                'Enjoyment',
                'Family',
                'Home',
                'Insurance',
                'One-off or Other',
                'Repayments',
                'Savings',
                'Transfers',
                'Transport',
                'Unknown',
            ],
        },
    });
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
        console.log(values);
        if (values.length) {
            setFilter(filter => ({ ...filter, tags: { l1: values } }));
        } else {
            setFilter(filter => ({ ...filter, tags: {} }));
        }
    }

    function handleChangeDateFrom(value) {
        setFilter(filter => ({ ...filter, date_from: value?.format('YYYY-MM-DD') }));
    }

    function handleChangeDateTo(value) {
        setFilter(filter => ({ ...filter, date_to: value?.format('YYYY-MM-DD') }));
    }

    function isLoading() {
        return !allTags.length || !data || !loaded;
    }

    function renderOptions(allTags) {
        return allTags.map(tag => <Option key={tag}>{tag}</Option>);
    }

    if (isLoading()) {
        return <em>Loading...</em>;
    }

    return (
        <Card loading={!loaded} style={{ marginTop: 10 }}>
            <Toolbar title={LABELS.breakdownTitle}>
                <div
                    style={{
                        display: 'flex',
                        justifyItems: 'end',
                        justifyContent: ' space-around',
                    }}
                >
                    <DatePicker
                        onChange={handleChangeDateFrom}
                        style={{
                            marginRight: '5px',
                        }}
                    >
                        From
                    </DatePicker>
                    <DatePicker
                        onChange={handleChangeDateTo}
                        style={{
                            marginRight: '5px',
                        }}
                    >
                        To
                    </DatePicker>
                    <Select
                        mode='multiple'
                        allowClear
                        style={{
                            minWidth: '200px',
                            maxWidth: '300px',
                            marginRight: '5px',
                        }}
                        placeholder='Filter by Tag'
                        onChange={handleChangeTagFilter}
                    >
                        {renderOptions(allTags)}
                    </Select>
                    <Button onClick={handleReload}>
                        <ReloadOutlined />
                    </Button>
                </div>
            </Toolbar>
            <Divider style={{ margin: '0 0 10px' }} />
            <Skeleton loading={isLoading()}>
                <div style={{ height: '500px' }}>
                    <Doughnut data={data.data} options={data.options} />
                </div>
            </Skeleton>
        </Card>
    );
}
