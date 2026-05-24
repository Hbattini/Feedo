import { gql } from "@apollo/client";

export const CREATE_CAT_PROFILE_MUTATION = gql`
  mutation CreateCatProfile($data: CreateCatProfileInput!) {
    createCatProfile(data: $data) {
      publicId
      name
      bornAt
    }
  }
`;
