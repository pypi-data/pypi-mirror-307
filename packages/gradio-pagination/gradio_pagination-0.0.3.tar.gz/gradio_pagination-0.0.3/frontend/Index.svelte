<svelte:options accessors={true} />

<script lang="ts">
	import type { Gradio } from "@gradio/utils";
	import type { LoadingStatus } from "@gradio/statustracker";
	import { tick } from "svelte";

	export let gradio: Gradio<{
		change: never;
		submit: never;
		input: never;
		value: string;
		clear_status: LoadingStatus;
	}>;

	// 输入属性
	export let value = "";
	const parseValue: (str: string) => ({total: number; page: number; page_size: number }) = str => {
		try {
			const obj = JSON.parse(str || '{}') as any
			return obj;
		} catch (error) {
			console.log(error)
			return { total: 0, page: 1, page_size: 10 };
		}
	}
	let total = 0, page = 1, page_size = 10;

	const page_size_options = [10, 20, 50, 100]; // 每页条数选择项
	let max_page: number; // 总页数

	$: value, trigger_change();

	// 处理页码按钮点击
	function handle_page_click(newPage: number) {
		if (newPage !== page) {
			page = newPage;
			value = JSON.stringify({ total, page, page_size })
		}
	}

	// 处理上一页和下一页
	function handle_prev_next(delta: number) {
		const newPage = page + delta;
		if (newPage >= 1 && newPage <= max_page) {
			page = newPage;
			value = JSON.stringify({ total, page, page_size })
		}
	}

	// 处理每页条数选择
	async function handle_page_size_change(event: Event) {
		const newSize = parseInt((event.target as HTMLSelectElement).value);
		if (newSize !== page_size) {
			page_size = newSize;
			page = 1; // 重置到第一页
			await tick(); // 确保 DOM 更新
			value = JSON.stringify({ total, page, page_size })
		}
	}

	// 触发 change 事件并通知 gradio
	async function trigger_change() {
		const pageInfo = parseValue(value)
		total = pageInfo.total
		page = pageInfo.page
		page_size = pageInfo.page_size
		max_page = Math.ceil(total / page_size)

		await tick(); // 确保 DOM 更新
		gradio.dispatch("change");
	}

	// 分页范围生成器
	function paginationRange(currentPage: number, totalPage: number): Array<number | string> {
		const range = [];
		if (totalPage <= 0) return range;
		const delta = 2; // 当前页两侧显示的页码数
		const left = Math.max(2, currentPage - delta);
		const right = Math.min(totalPage - 1, currentPage + delta);

		if (left > 2) range.push(1, '...');
		else range.push(1);

		for (let i = left; i <= right; i++) {
			range.push(i);
		}

		if (right < totalPage - 1) range.push('...', totalPage);
		else if (right === totalPage - 1) range.push(totalPage);

		return range;
	}
</script>

<div class="pagination">
	<span class="total">Total {total} Items</span>
	
	<button 
		class="nav-button" 
		disabled={page === 1} 
		on:click={() => handle_prev_next(-1)}
	>
		<div class="arrow-prev" />
	</button>

	{#each paginationRange(page, max_page) as pageNumber}
		{#if pageNumber === '...'}
			<span class="dots">...</span>
		{:else}
			<button
				class="page-button"
				class:selected={page === pageNumber}
				on:click={() => handle_page_click(Number(pageNumber))}
			>
				{pageNumber}
			</button>
		{/if}
	{/each}

	<button 
		class="nav-button" 
		disabled={page === max_page || max_page <= 0} 
		on:click={() => handle_prev_next(1)}
	>
		<div class="arrow-next" />
	</button>

	<select class="page-size-selector" on:change={handle_page_size_change}>
		{#each page_size_options as size}
			<option value={size} selected={size === page_size}>{size} per page</option>
		{/each}
	</select>
</div>

<style>
	.arrow-prev::before {
		content: "<";  /* 使用 CSS 实现 < */
		margin-right: 5px;
	}

	.arrow-next::after {
		content: ">";  /* 使用 CSS 实现 > */
		margin-left: 5px;
	}
	.pagination {
		display: flex;
		align-items: center;
		gap: 8px;
	}

	.total {
		margin-right: 8px;
		color: #333;
	}

	.nav-button,
	.page-button {
		padding: 5px 10px;
		border: 1px solid #ccc;
		background-color: white;
		cursor: pointer;
		border-radius: 4px;
		color: #333;
	}

	.page-button:hover,
	.page-button.selected {
		background-color: #f0f0f0;
	}

	.page-button.selected {
		font-weight: bold;
		color: #333;
	}

	.page-size-selector {
		margin-left: 8px;
		padding: 5px 30px;
		color: #999;
		border-radius: 4px;
		border: 1px solid #ccc;
	}
	
	.nav-button:disabled,
	.page-button:disabled {
		cursor: not-allowed;
		color: #999;
		background-color: #f9f9f9;
	}
	
	.dots {
		padding: 5px 10px;
		color: #666;
	}
</style>
