import Breakdown from 'components/breakdown';
import Layout from 'components/layout';
import { TransactionList } from 'components/transaction-list';

export default function Home() {
    return (
        <Layout>
            <TransactionList />
            <Breakdown />
        </Layout>
    );
}
