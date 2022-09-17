import { Button, Card, Divider, Select, DatePicker, Skeleton, Empty, Radio, Space } from 'antd';
const { Option } = Select;

import { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import 'chart.js/auto';
import { ReloadOutlined } from '@ant-design/icons';
import moment from 'moment';

import Toolbar from 'components/toolbar';
import { LABELS } from 'components/i18n';
import { makeStore } from 'util/store';

import { getAllTags, getBreakdown } from './data';
import { DEFAULT_MODE, MODES, STORE_ID } from './constants';

export default function Breakdown() {
    const store = makeStore(STORE_ID);

    const [loaded, setLoaded] = useState(true);
    const [data, setData] = useState(null);
    const [filter, setFilter] = useState({
        dat_from: store.get('dateFrom'),
        date_to: store.get('dateTo'),
        tags: { l1: store.get('tagFilter') },
    });
    const [reload, setReload] = useState(false);
    const [allTags, setAllTags] = useState([]);
    const [mode, setMode] = useState(store.get('mode') ?? DEFAULT_MODE);

    const dateFormat = 'YYYY-MM-DD';
    const defaultDateFrom = store.get('dateFrom')
        ? moment(store.get('dateFrom'), dateFormat)
        : undefined;

    const defaultDateTo = store.get('dateTo') ? moment(store.get('dateTo'), dateFormat) : undefined;

    useEffect(() => {
        console.log('useEffect 2');
        getAllTags().then(res => {
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
        console.log('handleChangeTagFilter');
        store.set('tagFilter', values);
        if (values.length) {
            setFilter(filter => ({ ...filter, tags: { l1: values } }));
        } else {
            setFilter(filter => ({ ...filter, tags: {} }));
        }
    }

    function handleChangeDateFrom(value) {
        console.log('handleChangeDateFrom');
        const date_from = value?.format('YYYY-MM-DD');
        store.set('dateFrom', date_from);
        setFilter(filter => ({ ...filter, date_from }));
    }

    function handleChangeDateTo(value) {
        console.log('handleChangeDateTo');
        const date_to = value?.format('YYYY-MM-DD');
        store.set('dateTo', date_to);
        setFilter(filter => ({ ...filter, date_to }));
    }

    function handleOnChangeMode(event) {
        const value = event.target.value;
        store.set('mode', value);
        console.log(value);
        setMode(value);
    }

    function isLoading() {
        return !allTags.length || !data || !loaded;
    }

    function renderOptions(allTags) {
        return allTags.map(tag => <Option key={tag}>{tag}</Option>);
    }

    function isEmpty() {
        return data?.data?.datasets[0]?.data?.length == 0;
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
                        justifyContent: 'space-around',
                    }}
                >
                    <DatePicker
                        onChange={handleChangeDateFrom}
                        style={{ marginRight: '5px' }}
                        defaultValue={defaultDateFrom}
                    >
                        From
                    </DatePicker>
                    <DatePicker
                        onChange={handleChangeDateTo}
                        style={{ marginRight: '5px' }}
                        defaultValue={defaultDateTo}
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
                        defaultValue={store.get('tagFilter')}
                    >
                        {renderOptions(allTags)}
                    </Select>
                    <Button onClick={handleReload}>
                        <ReloadOutlined />
                    </Button>
                    <Radio.Group onChange={handleOnChangeMode} value={mode}>
                        <Space direction='vertical' style={{ padding: 10 }}>
                            <Radio value={MODES.All}>{MODES.All}</Radio>
                            <Radio value={MODES.Monthly}>{MODES.Monthly}</Radio>
                        </Space>
                    </Radio.Group>
                </div>
            </Toolbar>
            <Divider style={{ margin: '0 0 10px' }} />
            <Skeleton loading={isLoading()}>
                {isEmpty() ? (
                    <Empty />
                ) : (
                    <div style={{ height: '500px' }}>
                        <Doughnut data={data.data} options={data.options} />
                    </div>
                )}
            </Skeleton>
        </Card>
    );
}
