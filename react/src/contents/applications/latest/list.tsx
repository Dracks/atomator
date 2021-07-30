import {
    EuiBasicTable,
    EuiBasicTableColumn,
    EuiButton,
    EuiFlexGroup,
    EuiFlexItem,
    EuiIcon,
    EuiLink,
    EuiSpacer,
    EuiTableDataType,
    formatDate,
} from "@elastic/eui"
import React from "react"
import { useHistory } from "react-router"

import { getRouterLinkProps } from "../../../routing"
import { GQLGqlBuild, useReleaseBuildMutation } from "../../../utils/graphql/generated"
import { getVerName } from "../versions/utils"

interface BuildListProps {
    buildsList: GQLGqlBuild[]
    reload: () => void
}

interface AppWithLinkProps {
    name: string
    id: number
}

const AppWithLink: React.FC<AppWithLinkProps> = ({ name, id }) => (
    <EuiLink {...getRouterLinkProps("/applications/" + id)}>{name}</EuiLink>
)

const FieldsList: (
    nr: ({ buildId: number }) => void,
    deploy: (buildId: number) => void,
) => Array<EuiBasicTableColumn<GQLGqlBuild>> = (newRelease, deployBuild) => [
    {
        name: "application",
        field: "application",
        render: AppWithLink,
    },
    {
        name: "Version",
        render: (build: GQLGqlBuild) => {
            return getVerName(build)
        },
    },
    {
        field: "date",
        name: "Creation",
        dataType: "date" as EuiTableDataType,
        render: (date: Date) => formatDate(date, "dateTime"),
    },
    {
        field: "release",
        name: "Release",
    },
    {
        field: "branch",
        name: "Branch",
        align: "center",
    },
    {
        name: "Actions",
        actions: [
            {
                name: "new release",
                description: "Set it as new release",
                onClick: item => newRelease({ buildId: item.id }),
                available: (item: GQLGqlBuild) => item.isReleasable,
            },
            {
                name: "Deploy",
                description: "Deploy to one environment",
                onClick: item => deployBuild(item.id),
                color: "danger",
            },
        ],
    },
]

const BuildListWithApp: React.FC<BuildListProps> = ({ buildsList, reload }) => {
    const history = useHistory()
    const [, releaseBuild] = useReleaseBuildMutation()
    const CbRelease = args =>
        releaseBuild(args).then(() => {
            reload()
        })

    return (
        <React.Fragment>
            <EuiFlexGroup alignItems="center" direction="rowReverse">
                <EuiFlexItem grow={false}>
                    <EuiButton onClick={reload} iconType="refresh" />
                </EuiFlexItem>
            </EuiFlexGroup>

            <EuiSpacer size="l" />

            <EuiBasicTable
                columns={FieldsList(CbRelease, buildId => {
                    history.push("/deploy/new/" + buildId)
                })}
                items={buildsList}
            />
        </React.Fragment>
    )
}

export default BuildListWithApp
