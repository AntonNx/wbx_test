import re
from datetime import datetime
import subprocess

shards_limits = {}

while True:
    input_str = input('Введите имя шарды и её лимит (в формате "shardname oldlimit", для прекращения ввода введите "end"): ')
    if input_str.lower() == 'end':
        break

    try:
        shard, limit = input_str.split()
        if not re.match("^[a-zA-Z0-9_-]+$", shard):
            raise ValueError("Неверный формат шарды. Используйте только буквы, цифры, дефисы и подчеркивания.")
        shards_limits[shard] = int(limit)
    except ValueError:
        print("Ошибка ввода. Пожалуйста, убедитесь, что вы вводите шарду в правильном формате (буквы, цифры, дефисы, подчеркивания).")

# Создаем текстовый файл
output_filename = "output_script.txt"
with open(output_filename, "w") as output_file:
    output_file.write("1. git pull\n")
    branch_name = datetime.today().strftime('%Y%m%d') + "_shards_limits"
    output_file.write(f"2. git checkout -b {branch_name} origin/master\n")
    output_file.write("3. Меняю значения в файлах\n")

    sellers_brands = []
    hbrands = []
    other = []

    for shard, limit in shards_limits.items():
        if 'hbrands' in shard:
            hbrands.append((shard, limit))
        elif 'brands' in shard or 'sellers' in shard:
            sellers_brands.append((shard, limit))
        else:
            other.append((shard, limit))

    for i, (shard, limit) in enumerate(sellers_brands + hbrands + other, start=1):
        shard_for_commit = shard.replace('_', '-')
        commit_message = f'{shard_for_commit}: up limits {limit} -> {limit + 100000} ({datetime.today().strftime("%Y-%m-%d")})'
        output_file.write(f"4.{i} git add 'ansible-playbooks/vars/default/{shard_for_commit}.yaml' && "
                          f"git commit -m '{commit_message}'\n")

    output_file.write(f"5. git push origin {branch_name}\n")
    output_file.write("6. перехожу по ссылке и создаю МР\n")

    sellers_brands_str = ','.join(shard.replace('_', '-') for shard, _ in sellers_brands)
    hbrands_str = ','.join(shard.replace('_', '-') for shard, _ in hbrands)
    other_str = ','.join(shard.replace('_', '-') for shard, _ in other)

    output_file.write(f"7.1 SHARDS=\"{sellers_brands_str}\" DATACENTER=\"dpcat,elcat\" "
                      f"COUNTRY=\"ru\" SERVICE_GROUP=\"catalog\" DEPLOY_TYPE=auto VERSION=auto ./run-pipeline.sh /dev/null\n")
    output_file.write(f"7.2 SHARDS=\"{hbrands_str}\" DATACENTER=\"elcat\" "
                      f"COUNTRY=\"ru\" SERVICE_GROUP=\"catalog\" DEPLOY_TYPE=auto VERSION=auto ./run-pipeline.sh /dev/null\n")
    output_file.write(f"7.3 SHARDS=\"{other_str}\" DATACENTER=\"prod\" "
                      f"COUNTRY=\"ru\" SERVICE_GROUP=\"catalog\" DEPLOY_TYPE=auto VERSION=auto ./run-pipeline.sh /dev/null\n")

# Открываем файл с помощью программы по умолчанию для просмотра текстовых файлов
subprocess.run(["notepad.exe", output_filename], check=True)
