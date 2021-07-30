export const getVerName = ({
    major,
    minor,
    patch,
}: {
    major: number
    minor: number
    patch: number
}) => `${major}.${minor}.${patch}`
