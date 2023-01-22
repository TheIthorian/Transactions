import { Card, Divider, Skeleton, Empty, Switch } from 'antd';

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
    const [groupTags, setGroupTags] = useState(true);

    useEffect(() => {
        getTimeline(filter, groupTags).then(setData).catch(setError);
    }, [filter, reload, groupTags]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleChangeGroupTags(checked) {
        setGroupTags(checked);
    }

    function isLoading() {
        return (!allTags || !data) && !error;
    }

    function isEmpty() {
        return (data?.data?.datasets[0]?.data?.length ?? 0) == 0;
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
            >
                <GroupSwitch onChange={handleChangeGroupTags} />
            </FilterToolbar>
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

function GroupSwitch({ onChange }) {
    return (
        <div
            style={{
                margin: '0 15px 0px 15px',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
            }}
        >
            <label>Group tags</label>
            <Switch style={{ width: 'fit-content' }} defaultChecked onChange={onChange} />
        </div>
    );
}
