import { Empty } from 'antd';
import { LABELS } from 'components/i18n';

export default function ({ text }) {
    if (!text) {
        text = LABELS.noDataError;
    }
    return <Empty image={Empty.PRESENTED_IMAGE_SIMPLE}>{text}</Empty>;
}
