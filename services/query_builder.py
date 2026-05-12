from schemas.search import SearchFilters


class QueryBuilder:
    @staticmethod
    def build(
        filters: SearchFilters,
    ) -> str:
        query_parts: list[str] = []

        if filters.name:
            query_parts.append(
                f"name contains '{filters.name}'",
            )

        if filters.mime_type:
            query_parts.append(
                f"mimeType='{filters.mime_type}'",
            )

        if filters.full_text:
            query_parts.append(
                f"fullText contains '{filters.full_text}'",
            )

        return " and ".join(query_parts)
