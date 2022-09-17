import { Button, Card, Divider, Select, DatePicker, Skeleton } from 'antd';
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
import { STORE_ID } from './constants';

export default function Breakdown() {
    const [loaded, setLoaded] = useState(true);
    const [data, setData] = useState(null);
    const [filter, setFilter] = useState(undefined);
    const [reload, setReload] = useState(false);
    const [allTags, setAllTags] = useState([]);
    const store = makeStore(STORE_ID);
    const dateFormat = 'YYYY-MM-DD';

    const storedFilter = {
        dat_from: store.get('dateFrom'),
        date_to: store.get('dateTo'),
        tags: { l1: store.get('tagFilter') },
    };

    useEffect(() => {
        console.log('useEffect 2');
        getAllTags().then(res => {
            setAllTags(res);
        });

        getBreakdown(filter ?? storedFilter)
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
                        defaultValue={
                            store.get('dateTo')
                                ? moment(store.get('dateTo'), dateFormat)
                                : undefined
                        }
                    >
                        From
                    </DatePicker>
                    <DatePicker
                        onChange={handleChangeDateTo}
                        style={{
                            marginRight: '5px',
                        }}
                        defaultValue={
                            store.get('dateTo')
                                ? moment(store.get('dateTo'), dateFormat)
                                : undefined
                        }
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
