import type { CodegenConfig } from "@graphql-codegen/cli";

const config: CodegenConfig = {
  schema: "../backend/schema.graphql",
  documents: ["src/graphql/**/*.ts"],
  generates: {
    "src/graphql/generated/": {
      preset: "client",
      presetConfig: {
        gqlTagName: "gql"
      }
    }
  }
};

export default config;
