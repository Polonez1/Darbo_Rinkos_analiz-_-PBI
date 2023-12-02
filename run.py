import click
from data_processing import ProcessingData


@click.group()
def cli():
    pass


@cli.command(name="cat")
@click.option("-o", "--output", is_flag=True, help="save .xlsx data")
@click.argument("path", default="./xlsx_output/", type=click.Path(file_okay=False))
def processing_cat(output, path):
    cat = ProcessingData()
    cvmarket, cvonline = cat.processing_cat()

    if output:
        cvmarket.to_excel(f"{path}/cvmarket_category.xlsx")
        cvonline.to_excel(f"{path}/cvonline_category.xlsx")
    else:
        print(cvmarket.head(1))
        print(cvonline.head(1))


@cli.command(name="data")
@click.option("-o", "--output", is_flag=True, help="save .xlsx data")
@click.argument("path", default="./xlsx_output/", type=click.Path(file_okay=False))
def processing_data(output, path):
    cat = ProcessingData()
    cvmarket, cvonline = cat.processing_main()
    if output:
        cvmarket.to_excel(f"{path}/cvmarket.xlsx")
        cvonline.to_excel(f"{path}/cvonline.xlsx")
    else:
        print(cvmarket.head(1))
        print(cvonline.head(1))


if __name__ == "__main__":
    cli()


# python run.py cat -o ./test/
