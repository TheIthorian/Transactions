import Layout from 'components/layout';
import { ToastHandler } from 'components/toast-handler';
import { CurrentUserProvider } from 'hooks/userContext';
import { Logout } from 'components/logout';
import { Budgets } from 'components/budgets';

export default function BudgetPage() {
    return (
        <CurrentUserProvider>
            <Layout>
                <ToastHandler />
                <Logout />
                <Budgets />
            </Layout>
        </CurrentUserProvider>
    );
}
