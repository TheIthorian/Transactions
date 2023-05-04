import { Button, DatePicker } from 'antd';
import { ReloadOutlined } from '@ant-design/icons';
import moment from 'moment';

import Toolbar from 'components/toolbar';
import { TagFilter } from 'components/tag-filter';
import NoSsr from 'components/nossr';

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
    excludeTagFilter = false,
}) {
    return (
        <Toolbar title={title}>
            <NoSsr>
                <div
                    style={{
                        display: 'flex',
                        justifyItems: 'end',
                        justifyContent: 'space-around',
                        alignItems: 'center',
                    }}
                >
                    <DatePicker
                        onChange={handleChangeDateFrom}
                        style={{ marginRight: '5px' }}
                        defaultValue={defaultDateFrom && moment(defaultDateFrom)}
                    />
                    <DatePicker
                        onChange={handleChangeDateTo}
                        style={{ marginRight: '5px' }}
                        defaultValue={defaultDateTo && moment(defaultDateTo)}
                    />
                    {!excludeTagFilter && (
                        <TagFilter
                            allTags={allTags}
                            defaultValue={defaultSelectedTags}
                            onChange={handleChangeTagFilter}
                        />
                    )}
                    <>{children}</>
                    <Button onClick={handleReload}>
                        <ReloadOutlined />
                    </Button>
                </div>
            </NoSsr>
        </Toolbar>
    );
}
