import { useEffect, useState } from 'react';
import { Card, Skeleton, Spin } from 'antd';
import { LoadingOutlined } from '@ant-design/icons';

import { useFilter } from 'hooks/filter';
import { DataGrid } from 'components/data-grid';
import { LABELS } from 'components/i18n';
import { Error } from 'components/error';
import { FilterToolbar } from 'components/filter-toolbar';

import { buildColumns } from './columnBuilder';
import { UPLOAD_HISTORY_GRID_STORE_ID } from './constants';
import { getUploads } from './data';

export function UploadHistory() {
    const {
        handleChangeTagFilter,
        handleChangeDateFrom,
        handleChangeDateTo,
        defaultDateFrom,
        defaultDateTo,
        filter,
        store,
    } = useFilter(UPLOAD_HISTORY_GRID_STORE_ID);

    const [reload, setReload] = useState(false);
    const [loading, setLoading] = useState(true);
    const [uploads, setUploads] = useState(null);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [error, setError] = useState(null);
    const [columns, setColumns] = useState([]);

    useEffect(() => {
        setLoading(true);
        getUploads(filter)
            .then(setUploads)
            .catch(setError)
            .finally(() => setLoading(false));
        setColumns(buildColumns({}));
    }, [filter, reload]);

    function handleReload() {
        setReload(reload => !reload);
    }

    function handleSelectRow(selectedRows) {
        setSelectedRowKeys(selectedRows);
    }

    if (error) {
        return <Error error={error} />;
    }

    if (loading) {
        return (
            <Card
                style={{ marginTop: 10 }}
                bodyStyle={{
                    padding: 5,
                    minHeight: 300,
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                }}
            >
                <div style={{ textAlign: 'center' }}>
                    <Spin indicator={<LoadingOutlined style={{ fontSize: 48 }} spin />} />
                </div>
            </Card>
        );
    }

    return (
        <Card style={{ marginTop: 10 }} bodyStyle={{ padding: 5 }}>
            <Skeleton loading={loading}>
                <DataGrid
                    dataSource={uploads}
                    columns={columns}
                    onSelectRow={handleSelectRow}
                    store={store}
                >
                    <FilterToolbar
                        title={LABELS.uploadHistoryGridTitle}
                        {...{
                            handleChangeTagFilter,
                            handleChangeDateFrom,
                            handleChangeDateTo,
                            defaultDateFrom,
                            defaultDateTo,
                            handleReload,
                            excludeTagFilter: true,
                        }}
                    ></FilterToolbar>
                </DataGrid>
            </Skeleton>
        </Card>
    );
}
