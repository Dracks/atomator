import {
    EuiBasicTable,
    EuiBasicTableColumn,
    EuiIcon,
    EuiLink,
    EuiTableDataType,
    formatDate,
} from "@elastic/eui"
import filesize from "filesize"
import React from "react"
import { useHistory } from "react-router"

import {
    GQLGqlBuild,
    GQLGqlFileInfo,
    useReleaseBuildMutation,
} from "../../../utils/graphql/generated"
import { getVerName } from "../versions/utils"

interface BuildListProps {
    buildsList: GQLGqlBuild[]
    reload: () => void
}
const FieldsList: (
    nr: ({ buildId: number }) => void,
    deploy: (buildId: number) => void,
) => Array<EuiBasicTableColumn<GQLGqlBuild>> = (newRelease, deployBuild) => [
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
        field: "file.size",
        name: "File size",
        render: (size: number) => filesize(size || 0),
    },
    {
        field: "release",
        name: "Release",
        align: "center",
    },
    {
        field: "branch",
        name: "Branch",
        align: "center",
    },
    {
        align: "center",
        field: "file",
        mobileOptions: {
            show: false,
        },
        name: "download",
        render: function Download(file: GQLGqlFileInfo) {
            return (
                <EuiLink href={file.url} target="_blank">
                    <EuiIcon type="download" />
                </EuiLink>
            )
        },
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
const BuildList: React.FC<BuildListProps> = ({ buildsList, reload }) => {
    const history = useHistory()
    const [, releaseBuild] = useReleaseBuildMutation()
    const CbRelease = args =>
        releaseBuild(args).then(() => {
            reload()
        })

    return (
        <EuiBasicTable
            columns={FieldsList(CbRelease, buildId => {
                history.push("/deploy/new/" + buildId)
            })}
            items={buildsList}
        />
    )
}

export default BuildList
