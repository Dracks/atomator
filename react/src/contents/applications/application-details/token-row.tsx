import { EuiFlexGroup, EuiFlexItem } from "@elastic/eui"
import React from "react"

import { GQLGqlToken } from "../../../utils/graphql/generated"

interface TokenRowProps {
    token: GQLGqlToken
}

const TokenRow: React.FC<TokenRowProps> = ({ token }) => (
    <EuiFlexGroup>
        <EuiFlexItem grow={2}>{token.name}</EuiFlexItem>
        <EuiFlexItem grow={8}>{token.token}</EuiFlexItem>
    </EuiFlexGroup>
)

export default TokenRow
