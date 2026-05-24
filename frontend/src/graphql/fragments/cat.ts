import { gql } from "@apollo/client";

export const CAT_SUMMARY_FRAGMENT = gql`
  fragment CatSummary on CatType {
    publicId
    name
    bornAt
  }
`;
