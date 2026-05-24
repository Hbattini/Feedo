import { gql } from "@apollo/client";

export const FOOD_SUMMARY_FRAGMENT = gql`
  fragment FoodSummary on FoodType {
    publicId
    brandName
    canonicalName
    chewyUrl
  }
`;
