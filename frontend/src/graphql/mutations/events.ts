import { gql } from "@apollo/client";

export const LOG_CAT_EVENT_MUTATION = gql`
  mutation LogCatEvent($data: LogCatEventInput!) {
    logCatEvent(data: $data)
  }
`;
