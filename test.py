from src.domain.business import BusinessEntity, BUSINESS_SIZE, BusinessDTO


def main():
    data = {
        "name": "Test Business",
        "segment": "Test Segment",
        "country_code": "US",
        "size": BUSINESS_SIZE.SMALL,
    }

    dto = BusinessDTO(**data)
    # dto = business.to_dto(flat=True)
    print(dto.model_dump())

    entity = BusinessEntity(props=dto)
    print(entity.model_dump())
    print(entity.to_dto(flat=True))


if __name__ == "__main__":
    main()
