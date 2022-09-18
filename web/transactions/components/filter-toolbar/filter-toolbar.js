import { Button, DatePicker } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';

import Toolbar from 'components/toolbar';
import { TagFilter } from 'components/tag-filter';

export function FilterToolbar({
    title,
    handleChangeTagFilter,
    handleChangeDateFrom,
    handleChangeDateTo,
    allTags,
    defaultSelectedTags,
    defaultDateFrom,
    defaultDateTo,
    children,
    handleReload,
}) {
    return (
        <Toolbar title={title}>
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
                <TagFilter
                    allTags={allTags}
                    defaultValue={defaultSelectedTags}
                    onChange={handleChangeTagFilter}
                />
                {children}
                <Button onClick={handleReload}>
                    <ReloadOutlined />
                </Button>
            </div>
        </Toolbar>
    );
}
