import propTypes from 'prop-types';
import { useEffect, useState } from 'react';

import { Divider, Skeleton, Table as AntTable } from 'antd';

import Empty from 'components/empty';

import { makeHandleTableChange } from './eventHandlers';
import { usePagination } from './hooks';

// Searching: https://ant.design/components/table/#components-table-demo-custom-filter-panel
export function DataGrid({ children, dataSource, columns, onSelectRow, store }) {
    const [loading, setLoading] = useState(true);
    const [selectedRowKeys, setSelectedRowKeys] = useState([]);

    useEffect(() => setLoading(!dataSource), [dataSource]);

    function handleSelectRow(record) {
        let newSelectedRowKeys;
        if (selectedRowKeys.includes(record.key)) {
            newSelectedRowKeys = selectedRowKeys.filter(key => key !== record.key);
        } else {
            newSelectedRowKeys = [...selectedRowKeys, record.key];
        }
        setSelectedRowKeys(newSelectedRowKeys);
        onSelectRow(newSelectedRowKeys);
    }

    const pagination = usePagination(store);
    const rowSelection = {
        selectedRowKeys: selectedRowKeys,
        onChange: setSelectedRowKeys,
    };

    function Table() {
        if (!dataSource?.length && !loading) return <Empty />;

        return (
            <Skeleton loading={loading}>
                <AntTable
                    {...{ rowSelection, dataSource, columns, pagination }}
                    onRow={record => ({
                        onClick: () => handleSelectRow(record),
                    })}
                    onChange={store && makeHandleTableChange(store)}
                    size='small'
                />
            </Skeleton>
        );
    }

    return (
        <>
            {children}
            <Divider style={{ margin: '0 0 10px' }} />
            <Table />
        </>
    );
}

DataGrid.defaultProps = {
    loading: false,
};

DataGrid.propTypes = {
    dataSource: propTypes.array,
    columns: propTypes.array.isRequired,
    onSelectRow: propTypes.func,
    store: propTypes.object,
};
