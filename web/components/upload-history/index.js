import { useEffect, useState } from 'react';
import { Card } from 'antd';

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
    const [uploads, setUploads] = useState(null);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);
    const [error, setError] = useState(null);
    const [columns, setColumns] = useState([]);

    useEffect(() => {
        getUploads(filter).then(setUploads).catch(setError);
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

    return (
        <Card style={{ marginTop: 10 }} bodyStyle={{ padding: 5 }}>
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
        </Card>
    );
}
