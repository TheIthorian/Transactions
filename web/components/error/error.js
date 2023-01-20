import propTypes from 'prop-types';
import { Alert } from 'antd';

export function Error({ error }) {
    console.error(error);
    if (Array.isArray(error)) {
        return (
            <>
                {error.map(e => (
                    <Alert message={e?.title} description={e?.message} type='error' showIcon />
                ))}
            </>
        );
    }

    return <Alert message={error?.title} description={error?.message} type='error' showIcon />;
}

Error.prototypes = {
    error: propTypes.object,
};
