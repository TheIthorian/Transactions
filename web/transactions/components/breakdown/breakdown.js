import { Card, Divider, Skeleton, Empty, Radio, Space } from 'antd';

import { useEffect, useState } from 'react';
import { Doughnut } from 'react-chartjs-2';
import 'chart.js/auto';

import { FilterToolbar } from 'components/filter-toolbar';
import { LABELS } from 'components/i18n';
import { makeStore } from 'util/store';
import { useFilter } from 'hooks/filter';

import { getBreakdown } from './data';
import { DEFAULT_MODE, MODES, STORE_ID } from './constants';

export default function Breakdown() {
    const store = makeStore(STORE_ID);

    const {
        handleChangeTagFilter,
        handleChangeDateFrom,
        handleChangeDateTo,
        allTags,
        defaultSelectedTags,
        defaultDateFrom,
        defaultDateTo,
        filter,
    } = useFilter(STORE_ID);

    const [reload, setReload] = useState(false);
    const [loaded, setLoaded] = useState(true);
    const [data, setData] = useState(null);
    const [mode, setMode] = useState(store.get('mode') ?? DEFAULT_MODE);
    const [error, setError] = useState(null);

    useEffect(() => {
        getBreakdown(filter, mode)
            .then(setData)
            .then(() => setLoaded(true))
            .catch(setError);
    }, [filter, reload, mode]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleOnChangeMode(event) {
        const value = event.target.value;
        store.set('mode', value);
        console.log(value);
        setMode(value);
    }

    function isLoading() {
        return (!allTags.length || !data || !loaded) && !error;
    }

    function isEmpty() {
        return data?.data?.datasets[0]?.data?.length == 0;
    }

    if (error) {
        return <Error error={error} />;
    }

    return (
        <Card loading={isLoading()} style={{ marginTop: 10 }}>
            <FilterToolbar
                title={LABELS.breakdownTitle}
                {...{
                    handleChangeTagFilter,
                    handleChangeDateFrom,
                    handleChangeDateTo,
                    allTags,
                    defaultSelectedTags,
                    defaultDateFrom,
                    defaultDateTo,
                }}
            >
                <Radio.Group onChange={handleOnChangeMode} value={mode}>
                    <Space direction='vertical' style={{ padding: 10 }}>
                        <Radio value={MODES.All}>{MODES.All}</Radio>
                        <Radio value={MODES.Monthly}>{MODES.Monthly}</Radio>
                    </Space>
                </Radio.Group>
            </FilterToolbar>
            <Divider style={{ margin: '0 0 10px' }} />
            <Skeleton loading={isLoading()}>
                {isEmpty() ? (
                    <Empty />
                ) : (
                    <div style={{ height: '500px' }}>
                        <Doughnut data={data?.data} options={data?.options} />
                    </div>
                )}
                <h2>Total: {'£' + data?.data.total?.toLocaleString()}</h2>
            </Skeleton>
        </Card>
    );
}
