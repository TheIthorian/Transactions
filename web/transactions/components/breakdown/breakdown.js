import { Button, Card, Divider, Select, Option, DatePicker, Skeleton, Space } from 'antd';
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

    function isLoading() {
        return !allTags.length || !data || !loaded;
    }

    if (isLoading()) {
        return <em>Loading...</em>;
    }

    return (
        <Card loading={!loaded} maxHeight='300px' maxWidth='100vw' marginTop={10}>
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
            <Skeleton loading={isLoading()}>
                <div
                    display='flex'
                    alignItems='center'
                    justifyContent='center'
                    style={{ height: '500px' }}
                >
                    <Doughnut data={data.data} options={data.options} />
                </div>
            </Skeleton>
        </Card>
    );
}
