import { EuiLoadingSpinner, EuiPage, EuiPageBody, EuiPageContent } from "@elastic/eui"
import React from "react"

const Loading = () => <EuiLoadingSpinner size="xl" />

export const LoadingPage = () => (
    <EuiPage>
        <EuiPageBody>
            <EuiPageContent verticalPosition="center" horizontalPosition="center">
                <Loading />
            </EuiPageContent>
        </EuiPageBody>
    </EuiPage>
)
export default Loading
