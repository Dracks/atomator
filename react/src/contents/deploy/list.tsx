import {
    EuiBasicTable,
    EuiBasicTableColumn,
    EuiPageBody,
    EuiPageContent,
    formatDate,
} from "@elastic/eui"
import React from "react"
import { useHistory } from "react-router"

import {
    GQLGqlExecutionOutput,
    useGetListDeploysQuery,
} from "../../utils/graphql/generated"

const FieldsList: (
    showDeploy: (i: number) => void,
) => Array<EuiBasicTableColumn<GQLGqlExecutionOutput>> = showDeploy => [
    {
        field: "date",
        name: "Date",
        dataType: "date",
        render: (date: Date) => formatDate(date, "dateTime"),
    },
    {
        field: "application.name",
        name: "application",
    },
    {
        field: "status",
        name: "Status",
    },
    {
        name: "Environment",
        field: "environment.environment",
    },
    {
        name: "Actions",
        actions: [
            {
                name: "Show",
                description: "Show the output",
                onClick: item => showDeploy(item.id),
            },
        ],
    },
]
const DeployList: React.FC<{}> = () => {
    const [response] = useGetListDeploysQuery({ requestPolicy: "network-only" })
    const history = useHistory()

    return (
        <EuiPageContent>
            <EuiPageBody>
                <EuiBasicTable
                    columns={FieldsList(id => {
                        history.push("/deploy/" + id)
                    })}
                    items={
                        (response.data?.deployments as Array<GQLGqlExecutionOutput>) ||
                        []
                    }
                />
            </EuiPageBody>
        </EuiPageContent>
    )
}
export default DeployList
