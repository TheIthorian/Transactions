import { Card, Divider, Skeleton, Empty } from 'antd';

import { useEffect, useState } from 'react';
import { Bar } from 'react-chartjs-2';
import 'chart.js/auto';

import { useFilter } from 'hooks/filter';
import { LABELS } from 'components/i18n';
import { Error } from 'components/error';
import { FilterToolbar } from 'components/filter-toolbar';

import { STORE_ID } from './constants';
import { getTimeline } from './data';

export function TransactionTimeline() {
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

    const [data, setData] = useState(null);
    const [reload, setReload] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        getTimeline(filter).then(setData).catch(setError);
    }, [filter, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function isLoading() {
        return (!allTags.length || !data) && !error;
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
                title={LABELS.timelineTitle}
                {...{
                    handleChangeTagFilter,
                    handleChangeDateFrom,
                    handleChangeDateTo,
                    allTags,
                    defaultSelectedTags,
                    defaultDateFrom,
                    defaultDateTo,
                    handleReload,
                }}
            />
            <Divider style={{ margin: '0 0 10px' }} />
            <Skeleton loading={isLoading()}>
                {isEmpty() ? (
                    <Empty />
                ) : (
                    <div style={{ height: '500px' }}>
                        <Bar data={data?.data} options={data?.options} />
                    </div>
                )}
            </Skeleton>
        </Card>
    );
}
