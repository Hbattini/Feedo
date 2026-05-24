import { gql } from "@apollo/client";

import { CAT_SUMMARY_FRAGMENT } from "../fragments/cat";

export const MY_CATS_QUERY = gql`
  ${CAT_SUMMARY_FRAGMENT}
  query MyCats {
    myCats {
      ...CatSummary
    }
  }
`;
