import { LABELS } from 'components/i18n';
import {
    makeSizeRenderer,
    makeDateRenderer,
    makeStatusRenderer,
    makeFilenameRenderer,
} from './renderers';

export function buildColumns(store) {
    return [
        {
            title: LABELS.id,
            dataIndex: 'id',
            key: 'id',
        },
        {
            title: LABELS.uploadFilename,
            dataIndex: 'file_name',
            key: 'file_name',
            render: makeFilenameRenderer(),
        },
        {
            title: LABELS.uploadSize,
            dataIndex: 'size',
            key: 'size',
            render: makeSizeRenderer(),
        },
        {
            title: LABELS.uploadDate,
            dataIndex: 'date',
            key: 'date',
            render: makeDateRenderer(),
        },
        {
            title: LABELS.uploadHash,
            dataIndex: 'md5',
            key: 'hash',
        },
        {
            title: LABELS.uploadStatus,
            dataIndex: 'status',
            key: 'status',
            render: makeStatusRenderer(),
        },
    ];
}
