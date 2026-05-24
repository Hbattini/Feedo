import { gql } from "@apollo/client";

import { FOOD_SUMMARY_FRAGMENT } from "../fragments/food";

export const FOOD_CATALOG_QUERY = gql`
  ${FOOD_SUMMARY_FRAGMENT}
  query FoodCatalog($first: Int!, $after: String) {
    foodCatalog(first: $first, after: $after) {
      ...FoodSummary
    }
  }
`;
