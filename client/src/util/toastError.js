import {toast} from 'react-toastify';

export const toastError = (errorResponse) => {
    const errors = errorResponse?.data?.detail;

    if (Array.isArray(errors)) {
        errors.forEach(error => {
            const fieldName = error.loc[1];
            const shortMessage = error.msg.split(':')[0];
            const message = `${fieldName}: ${shortMessage}`;
            toast.error(message);
        });
    } else {
        toast.error(errors)
    }
};
