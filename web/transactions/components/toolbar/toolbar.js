import propTypes from 'prop-types';
import { Space } from 'antd';

import styles from './toolbar.module.css';

export default function Toolbar({ title, children }) {
    return (
        <Space width='100%' align='baseline' className={styles.toolbar}>
            <h1>{title}</h1>
            <Space style={{ width: '100%', justifyContent: 'end' }}>{children}</Space>
        </Space>
    );
}

Toolbar.propTypes = {
    title: propTypes.string.isRequired,
    children: propTypes.element,
};
