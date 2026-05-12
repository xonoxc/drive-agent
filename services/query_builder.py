from schemas.search import SearchFilters


class QueryBuilder:
    @staticmethod
    def build(
        filters: SearchFilters,
    ) -> str:
        query_parts: list[str] = []

        if filters.exact_name:
            query_parts.append(
                f"name = '{filters.exact_name}'",
            )

        if filters.partial_name:
            query_parts.append(
                f"name contains '{filters.partial_name}'",
            )

        if filters.mime_type:
            query_parts.append(
                f"mimeType = '{filters.mime_type}'",
            )

        if filters.full_text:
            query_parts.append(
                f"fullText contains '{filters.full_text}'",
            )

        if filters.modified_after:
            query_parts.append(
                f"modifiedTime >= '{filters.modified_after.isoformat()}'",
            )

        return " and ".join(query_parts)
