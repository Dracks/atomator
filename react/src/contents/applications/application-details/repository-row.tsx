import { EuiFlexGroup, EuiFlexItem } from "@elastic/eui"
import React from "react"

import { GQLGqlRepository } from "../../../utils/graphql/generated"

interface RepositoryRowProps {
    repo: GQLGqlRepository
}

const RepositoryRow: React.FC<RepositoryRowProps> = ({ repo }) => (
    <EuiFlexGroup>
        <EuiFlexItem grow={3}>{repo.name}</EuiFlexItem>
        <EuiFlexItem grow={3}>{repo.provider}</EuiFlexItem>
        <EuiFlexItem grow={6}>{repo.url}</EuiFlexItem>
    </EuiFlexGroup>
)

export default RepositoryRow
