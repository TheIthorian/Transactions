import propTypes from 'prop-types';
import { Alert } from 'antd';

export function Error({ error }) {
    return <Alert message={error?.title} description={error?.message} type='error' showIcon />;
}

Error.prototypes = {
    error: propTypes.object,
};
