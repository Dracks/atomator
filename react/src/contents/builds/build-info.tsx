import {
    EuiBadge,
    EuiDescriptionList,
    EuiFlexItem,
    EuiText,
    formatDate,
} from "@elastic/eui"
import React from "react"

import {
    GQLGqlApplication,
    GQLGqlBuild,
    GQLGqlChange,
} from "../../utils/graphql/generated"
import { getVerName } from "../applications/versions/utils"

type AliasApplication = Pick<GQLGqlApplication, "name">

type AliasChanges = Pick<GQLGqlChange, "type" | "description">
type AliasBuild = Pick<
    GQLGqlBuild,
    "major" | "minor" | "patch" | "date" | "release"
> & { application: AliasApplication; changes: AliasChanges[] }

const BuildInfo: React.FC<{ build: AliasBuild }> = ({ build }) => {
    return (
        <EuiFlexItem>
            <EuiText>
                <h2>{build.application.name}</h2>
                {formatDate(build.date, "dateTime")}
                <EuiBadge color={build.release ? "primary" : "secondary"}>
                    {getVerName(build)}
                </EuiBadge>
                <h3>Changes</h3>
            </EuiText>
            <ul>
                {build.changes.map(({ type, description }, idx) => (
                    <li key={idx}>
                        {type}:{description}
                    </li>
                ))}
            </ul>
        </EuiFlexItem>
    )
}

export default BuildInfo
