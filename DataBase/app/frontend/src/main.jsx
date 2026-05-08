import React, { useEffect, useMemo, useState } from 'react';
import { createRoot } from 'react-dom/client';
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';
import {
  Activity,
  ArrowUpRight,
  BarChart3,
  BookOpen,
  Building2,
  CheckCircle2,
  ChevronDown,
  ChevronsUpDown,
  Command,
  Database,
  FileText,
  Gauge,
  LayoutDashboard,
  Loader2,
  PenLine,
  Plus,
  RefreshCw,
  Search,
  ShieldCheck,
  Sparkles,
  Users,
  Workflow,
  X,
  Zap,
} from 'lucide-react';
import './styles.css';

const API_URL = import.meta.env.VITE_API_URL ?? 'http://127.0.0.1:8000';

const navItems = [
  { id: 'overview', label: 'Обзор', icon: LayoutDashboard, hint: 'Сводка' },
  { id: 'orders', label: 'Заказы', icon: FileText, hint: 'Операции' },
  { id: 'customers', label: 'Клиенты', icon: Users, hint: 'CRM' },
  { id: 'editions', label: 'Издания', icon: BookOpen, hint: 'Каталог' },
  { id: 'typographies', label: 'Типографии', icon: Building2, hint: 'Загрузка' },
  { id: 'authors', label: 'Авторы', icon: PenLine, hint: 'Справочник' },
  { id: 'analytics', label: 'Аналитика', icon: BarChart3, hint: 'VIEW' },
];

const demo = {
  dashboard: {
    totals: { total_orders: 6, open_orders: 2, completed_orders: 4 },
    active_typographies: 3,
    latest_orders: [
      { order_id: 6, customer_name: 'Publishing Plus LLC', product_type: 'textbook', edition_title: 'Database Systems Workshop', typography_name: 'Amber Press', received_at: '2025-03-20', completed_at: '2025-03-27', is_completed: true },
      { order_id: 5, customer_name: 'Alexey Petrov', product_type: 'auto_order', edition_title: 'Database Systems Workshop', typography_name: 'University Print House', received_at: '2025-03-15', completed_at: null, is_completed: false },
      { order_id: 4, customer_name: 'Elena Smirnova', product_type: 'brochure', edition_title: 'Modern Pedagogy Guide', typography_name: 'Baltic Typography', received_at: '2025-03-01', completed_at: null, is_completed: false },
      { order_id: 3, customer_name: 'Baltic Education Center', product_type: 'catalog', edition_title: 'Regional Science Catalog', typography_name: 'University Print House', received_at: '2025-02-05', completed_at: '2025-02-09', is_completed: true },
    ],
    customer_stats: [
      { customer_id: 1, customer_name: 'Alexey Petrov', orders_count: 2, open_orders_count: 1, completed_orders_count: 1 },
      { customer_id: 2, customer_name: 'Publishing Plus LLC', orders_count: 2, open_orders_count: 0, completed_orders_count: 2 },
      { customer_id: 3, customer_name: 'Baltic Education Center', orders_count: 1, open_orders_count: 0, completed_orders_count: 1 },
      { customer_id: 4, customer_name: 'Elena Smirnova', orders_count: 1, open_orders_count: 1, completed_orders_count: 0 },
    ],
    typography_workload: [
      { typography_id: 1, typography_name: 'Baltic Typography', orders_count: 2, first_order_date: '2025-01-10', last_order_date: '2025-03-01' },
      { typography_id: 2, typography_name: 'Amber Press', orders_count: 2, first_order_date: '2025-01-12', last_order_date: '2025-03-20' },
      { typography_id: 3, typography_name: 'University Print House', orders_count: 2, first_order_date: '2025-02-05', last_order_date: '2025-03-15' },
    ],
  },
};

demo.orders = demo.dashboard.latest_orders;
demo.customers = [
  { id: 1, name: 'Alexey Petrov', customer_type: 'Person', customer_type_code: 'person', contact_name: 'Alexey Petrov', address: 'Kaliningrad, Yuzhnaya 14', phone: '+79991112233' },
  { id: 2, name: 'Publishing Plus LLC', customer_type: 'Organization', customer_type_code: 'organization', contact_name: 'L. Egorova', address: 'Kaliningrad, Baltiyskaya 9', phone: '+74012345678' },
  { id: 3, name: 'Baltic Education Center', customer_type: 'Organization', customer_type_code: 'organization', contact_name: 'M. Romanova', address: 'Kaliningrad, Universitetskaya 3', phone: '+74012300011' },
  { id: 4, name: 'Elena Smirnova', customer_type: 'Person', customer_type_code: 'person', contact_name: 'Elena Smirnova', address: 'Svetlogorsk, Morskaya 5', phone: '+79990007766' },
];
demo.editions = [
  { id: 1, title: 'Russian Literature of the 20th Century', sheet_count: 15, circulation: 3000 },
  { id: 2, title: 'History of European States', sheet_count: 22, circulation: 1500 },
  { id: 3, title: 'Database Systems Workshop', sheet_count: 12, circulation: 2000 },
  { id: 4, title: 'Regional Science Catalog', sheet_count: 8, circulation: 1200 },
  { id: 5, title: 'Modern Pedagogy Guide', sheet_count: 18, circulation: 2500 },
];
demo.typographies = [
  { id: 1, name: 'Baltic Typography', address: 'Kaliningrad, Mira 10', phone: '+74012000001' },
  { id: 2, name: 'Amber Press', address: 'Kaliningrad, Portovaya 7', phone: '+74012000002' },
  { id: 3, name: 'University Print House', address: 'Kaliningrad, Academic 2', phone: '+74012000003' },
];
demo.authors = [
  { id: 1, full_name: 'Igor Sidorov', address: 'Sovetsk, Naberezhnaya 5', phone: '+79995550101', bio: 'Author of study literature' },
  { id: 2, full_name: 'Elena Markova', address: 'Guryevsk, Lesnaya 8', phone: '+79997773322', bio: 'Specialist in history editions' },
  { id: 3, full_name: 'Pavel Orlov', address: 'Kaliningrad, Chernyakhovskogo 12', phone: '+79994443322', bio: 'Database lecturer and methodologist' },
  { id: 4, full_name: 'Marina Volkova', address: 'Zelenogradsk, Parkovaya 11', phone: '+79993334455', bio: 'Compiler of educational catalogs' },
];
demo.analytics = {
  customerStats: demo.dashboard.customer_stats,
  typographyWorkload: demo.dashboard.typography_workload,
  openOrders: demo.orders.filter((order) => !order.is_completed),
  completedOrders: demo.orders.filter((order) => order.is_completed),
};

function demoFor(path) {
  if (path.startsWith('/dashboard')) return demo.dashboard;
  if (path.startsWith('/orders')) return demo.orders;
  if (path.startsWith('/customers')) return demo.customers;
  if (path.startsWith('/editions')) return demo.editions;
  if (path.startsWith('/typographies')) return demo.typographies;
  if (path.startsWith('/authors')) return demo.authors;
  if (path.startsWith('/analytics/customer-stats')) return demo.analytics.customerStats;
  if (path.startsWith('/analytics/typography-workload')) return demo.analytics.typographyWorkload;
  if (path.startsWith('/analytics/open-orders')) return demo.analytics.openOrders;
  if (path.startsWith('/analytics/completed-orders')) return demo.analytics.completedOrders;
  return null;
}

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers ?? {}) },
    ...options,
  });
  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.detail ?? `HTTP ${response.status}`);
  }
  return response.json();
}

function useApi(path, deps = []) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [demoMode, setDemoMode] = useState(false);
  const [version, setVersion] = useState(0);

  useEffect(() => {
    let ignore = false;
    setLoading(true);
    setError('');
    request(path)
      .then((result) => {
        if (!ignore) {
          setData(result);
          setDemoMode(false);
        }
      })
      .catch((err) => {
        const fallback = demoFor(path);
        if (!ignore && fallback) {
          setData(fallback);
          setDemoMode(true);
          setError(err.message);
        } else if (!ignore) {
          setError(err.message);
        }
      })
      .finally(() => {
        if (!ignore) setLoading(false);
      });
    return () => {
      ignore = true;
    };
  }, [path, version, ...deps]);

  return { data, loading, error, demoMode, reload: () => setVersion((value) => value + 1) };
}

function formatDate(value) {
  if (!value) return 'в работе';
  return new Date(value).toLocaleDateString('ru-RU');
}

function number(value) {
  return new Intl.NumberFormat('ru-RU').format(Number(value ?? 0));
}

function statusLabel(completed) {
  return completed ? 'Завершён' : 'В работе';
}

function StatusBadge({ completed }) {
  return <span className={completed ? 'badge badge-done' : 'badge-open badge'}>{statusLabel(completed)}</span>;
}

function DemoBanner({ show, message }) {
  if (!show) return null;
  return (
    <div className="demo-banner">
      <Sparkles size={17} />
      <span>Демо-режим: API недоступен, интерфейс показывает демонстрационные данные.</span>
      <small>{message}</small>
    </div>
  );
}

function Toolbar({ title, subtitle, onRefresh, children, demoMode, error }) {
  return (
    <>
      <div className="toolbar">
        <div>
          <h2>{title}</h2>
          <p>{subtitle}</p>
        </div>
        <div className="toolbar-actions">
          {children}
          {onRefresh && (
            <button className="icon-button" onClick={onRefresh} title="Обновить данные">
              <RefreshCw size={18} />
            </button>
          )}
        </div>
      </div>
      <DemoBanner show={demoMode} message={error} />
    </>
  );
}

function LoadingState() {
  return (
    <div className="state">
      <Loader2 className="spin" size={22} />
      <span>Загрузка данных</span>
    </div>
  );
}

function ErrorState({ message }) {
  return (
    <div className="error">
      <X size={18} />
      Ошибка: {message}
    </div>
  );
}

function DataTable({ columns, rows, empty = 'Нет данных' }) {
  const [sort, setSort] = useState({ key: columns[0]?.key, dir: 'asc' });
  const sortedRows = useMemo(() => {
    const copy = [...rows];
    if (!sort.key) return copy;
    copy.sort((a, b) => {
      const left = a[sort.key] ?? '';
      const right = b[sort.key] ?? '';
      const result = String(left).localeCompare(String(right), 'ru', { numeric: true, sensitivity: 'base' });
      return sort.dir === 'asc' ? result : -result;
    });
    return copy;
  }, [rows, sort]);

  function toggle(key) {
    setSort((current) => ({ key, dir: current.key === key && current.dir === 'asc' ? 'desc' : 'asc' }));
  }

  return (
    <div className="table-wrap">
      <table>
        <thead>
          <tr>
            {columns.map((column) => (
              <th key={column.key}>
                <button className="th-sort" onClick={() => toggle(column.key)}>
                  {column.title}
                  <ChevronsUpDown size={13} />
                </button>
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {sortedRows.length === 0 && (
            <tr>
              <td colSpan={columns.length} className="empty">
                {empty}
              </td>
            </tr>
          )}
          {sortedRows.map((row, index) => (
            <tr key={row.id ?? row.order_id ?? row.customer_id ?? row.typography_id ?? `${row.name}-${index}`}>
              {columns.map((column) => (
                <td key={column.key}>{column.render ? column.render(row) : row[column.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Metric({ label, value, icon: Icon, accent, detail }) {
  return (
    <section className="metric" style={{ '--accent': accent }}>
      <div className="metric-copy">
        <span>{label}</span>
        <strong>{number(value)}</strong>
        <small>{detail}</small>
      </div>
      <div className="metric-icon">
        <Icon size={24} />
      </div>
    </section>
  );
}

function Spotlight({ dashboard, setActive }) {
  const openRate = dashboard.totals.total_orders
    ? Math.round((dashboard.totals.open_orders / dashboard.totals.total_orders) * 100)
    : 0;
  return (
    <section className="spotlight">
      <div>
        <span className="pill"><Zap size={15} /> live publishing ops</span>
        <h2>Операционный центр издательства</h2>
        <p>Заказы, справочники, процедуры PL/pgSQL и аналитика VIEW собраны в одном интерфейсе для реальной работы с базой.</p>
        <div className="spotlight-actions">
          <button className="primary lift" onClick={() => setActive('orders')}>
            <Plus size={17} />
            Создать заказ
          </button>
          <button className="ghost-button" onClick={() => setActive('analytics')}>
            <BarChart3 size={17} />
            Смотреть аналитику
          </button>
        </div>
      </div>
      <div className="radar-card">
        <div className="radar-value">{openRate}%</div>
        <span>доля заказов в работе</span>
        <div className="progress-ring" style={{ '--progress': `${openRate * 3.6}deg` }} />
      </div>
    </section>
  );
}

function Overview({ setActive }) {
  const { data, loading, error, demoMode, reload } = useApi('/dashboard');
  if (loading) return <LoadingState />;
  if (!data) return <ErrorState message={error} />;

  const workload = data.typography_workload.map((item) => ({
    name: item.typography_name.replace(' Print House', ''),
    orders: Number(item.orders_count),
  }));
  const flow = data.latest_orders
    .slice()
    .reverse()
    .map((item, index) => ({
      name: `#${item.order_id}`,
      completed: item.is_completed ? index + 1 : index,
      open: item.is_completed ? index : index + 1,
    }));
  const pieData = [
    { name: 'Завершены', value: Number(data.totals.completed_orders), color: '#2f9e75' },
    { name: 'В работе', value: Number(data.totals.open_orders), color: '#f2b441' },
  ];

  return (
    <>
      <Toolbar
        title="Обзор"
        subtitle="Сводка по заказам, клиентам и загрузке типографий"
        onRefresh={reload}
        demoMode={demoMode}
        error={error}
      />
      <Spotlight dashboard={data} setActive={setActive} />
      <div className="metrics-grid">
        <Metric label="Всего заказов" value={data.totals.total_orders} accent="#6d5dfc" icon={Database} detail="операционный контур" />
        <Metric label="В работе" value={data.totals.open_orders} accent="#f2b441" icon={Activity} detail="требуют внимания" />
        <Metric label="Завершено" value={data.totals.completed_orders} accent="#2f9e75" icon={CheckCircle2} detail="закрытый цикл" />
        <Metric label="Типографии" value={data.active_typographies} accent="#e15c74" icon={Building2} detail="активная загрузка" />
      </div>
      <div className="dashboard-grid">
        <section className="panel chart-panel wide">
          <div className="panel-heading">
            <div>
              <h3>Динамика заказов</h3>
              <p>Состояние последних операций</p>
            </div>
            <span className="panel-tag">VIEW order_details</span>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <AreaChart data={flow}>
              <defs>
                <linearGradient id="completedFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#2f9e75" stopOpacity={0.35} />
                  <stop offset="95%" stopColor="#2f9e75" stopOpacity={0.02} />
                </linearGradient>
                <linearGradient id="openFill" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="5%" stopColor="#f2b441" stopOpacity={0.4} />
                  <stop offset="95%" stopColor="#f2b441" stopOpacity={0.02} />
                </linearGradient>
              </defs>
              <CartesianGrid strokeDasharray="3 3" stroke="#d9e1e7" />
              <XAxis dataKey="name" stroke="#70828e" />
              <YAxis stroke="#70828e" />
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #d9e1e7' }} />
              <Area type="monotone" dataKey="completed" name="Завершено" stroke="#2f9e75" fill="url(#completedFill)" strokeWidth={3} />
              <Area type="monotone" dataKey="open" name="В работе" stroke="#f2b441" fill="url(#openFill)" strokeWidth={3} />
            </AreaChart>
          </ResponsiveContainer>
        </section>
        <section className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <h3>Статус заказов</h3>
              <p>Выполнение</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <PieChart>
              <Pie data={pieData} dataKey="value" innerRadius={62} outerRadius={88} paddingAngle={4}>
                {pieData.map((entry) => <Cell key={entry.name} fill={entry.color} />)}
              </Pie>
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #d9e1e7' }} />
            </PieChart>
          </ResponsiveContainer>
          <div className="legend-row">
            {pieData.map((item) => (
              <span key={item.name}><i style={{ background: item.color }} />{item.name}</span>
            ))}
          </div>
        </section>
        <section className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <h3>Типографии</h3>
              <p>Нагрузка</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={260}>
            <BarChart data={workload} layout="vertical" margin={{ left: 16 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d9e1e7" />
              <XAxis type="number" allowDecimals={false} stroke="#70828e" />
              <YAxis type="category" dataKey="name" width={110} stroke="#70828e" />
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #d9e1e7' }} />
              <Bar dataKey="orders" name="Заказы" radius={[0, 10, 10, 0]} fill="#6d5dfc" />
            </BarChart>
          </ResponsiveContainer>
        </section>
        <section className="panel wide">
          <div className="panel-heading">
            <div>
              <h3>Последние заказы</h3>
              <p>Нажми на заголовок таблицы для сортировки</p>
            </div>
            <button className="ghost-button compact" onClick={() => setActive('orders')}>
              Открыть
              <ArrowUpRight size={15} />
            </button>
          </div>
          <DataTable
            rows={data.latest_orders}
            columns={[
              { key: 'order_id', title: '№' },
              { key: 'customer_name', title: 'Клиент' },
              { key: 'edition_title', title: 'Издание' },
              { key: 'typography_name', title: 'Типография' },
              { key: 'received_at', title: 'Дата', render: (row) => formatDate(row.received_at) },
              { key: 'completed_at', title: 'Статус', render: (row) => <StatusBadge completed={row.is_completed} /> },
            ]}
          />
        </section>
      </div>
    </>
  );
}

function Orders() {
  const [status, setStatus] = useState('all');
  const { data, loading, error, demoMode, reload } = useApi(`/orders?status=${status}`, [status]);
  const [form, setForm] = useState({
    customer_id: '',
    product_type_code: 'textbook',
    edition_id: '',
    typography_id: '',
    received_at: new Date().toISOString().slice(0, 10),
    completed_at: '',
  });
  const [complete, setComplete] = useState({ order_id: '', completed_at: new Date().toISOString().slice(0, 10) });
  const [message, setMessage] = useState('');

  async function createOrder(event) {
    event.preventDefault();
    setMessage('');
    request('/orders', {
      method: 'POST',
      body: JSON.stringify({
        customer_id: Number(form.customer_id),
        product_type_code: form.product_type_code,
        edition_id: Number(form.edition_id),
        typography_id: form.typography_id ? Number(form.typography_id) : null,
        received_at: form.received_at,
        completed_at: form.completed_at || null,
      }),
    })
      .then(() => {
        setMessage('Заказ создан');
        reload();
      })
      .catch((err) => setMessage(err.message));
  }

  async function completeOrder(event) {
    event.preventDefault();
    setMessage('');
    request(`/orders/${complete.order_id}/complete`, {
      method: 'POST',
      body: JSON.stringify({ completed_at: complete.completed_at }),
    })
      .then(() => {
        setMessage('Заказ завершён');
        reload();
      })
      .catch((err) => setMessage(err.message));
  }

  return (
    <>
      <Toolbar title="Заказы" subtitle="Создание, фильтрация и завершение заказов через PL/pgSQL procedures" onRefresh={reload} demoMode={demoMode} error={error}>
        <div className="segmented">
          {[
            ['all', 'Все'],
            ['open', 'В работе'],
            ['completed', 'Завершённые'],
          ].map(([item, label]) => (
            <button key={item} className={status === item ? 'active' : ''} onClick={() => setStatus(item)}>
              {label}
            </button>
          ))}
        </div>
      </Toolbar>
      {message && <div className="notice">{message}</div>}
      <div className="forms-grid premium">
        <form className="panel form-panel" onSubmit={createOrder}>
          <h3><Plus size={18} /> Создать заказ</h3>
          <div className="field-row">
            <label>Клиент ID<input value={form.customer_id} onChange={(e) => setForm({ ...form, customer_id: e.target.value })} required /></label>
            <label>Издание ID<input value={form.edition_id} onChange={(e) => setForm({ ...form, edition_id: e.target.value })} required /></label>
            <label>Типография ID<input value={form.typography_id} onChange={(e) => setForm({ ...form, typography_id: e.target.value })} /></label>
          </div>
          <div className="field-row">
            <label>Тип продукции<input value={form.product_type_code} onChange={(e) => setForm({ ...form, product_type_code: e.target.value })} required /></label>
            <label>Принят<input type="date" value={form.received_at} onChange={(e) => setForm({ ...form, received_at: e.target.value })} required /></label>
            <label>Завершён<input type="date" value={form.completed_at} onChange={(e) => setForm({ ...form, completed_at: e.target.value })} /></label>
          </div>
          <button className="primary lift" type="submit"><Workflow size={17} />Запустить процедуру</button>
        </form>
        <form className="panel form-panel compact-form" onSubmit={completeOrder}>
          <h3><CheckCircle2 size={18} /> Завершить заказ</h3>
          <label>Заказ ID<input value={complete.order_id} onChange={(e) => setComplete({ ...complete, order_id: e.target.value })} required /></label>
          <label>Дата завершения<input type="date" value={complete.completed_at} onChange={(e) => setComplete({ ...complete, completed_at: e.target.value })} required /></label>
          <button className="primary lift" type="submit"><ShieldCheck size={17} />Завершить</button>
        </form>
      </div>
      {loading ? <LoadingState /> : !data ? <ErrorState message={error} /> : (
        <section className="panel">
          <div className="panel-heading">
            <div>
              <h3>Реестр заказов</h3>
              <p>Данные из view_order_details</p>
            </div>
          </div>
          <DataTable
            rows={data}
            columns={[
              { key: 'order_id', title: '№' },
              { key: 'customer_name', title: 'Клиент' },
              { key: 'product_type', title: 'Тип' },
              { key: 'edition_title', title: 'Издание' },
              { key: 'typography_name', title: 'Типография' },
              { key: 'received_at', title: 'Принят', render: (row) => formatDate(row.received_at) },
              { key: 'completed_at', title: 'Статус', render: (row) => <StatusBadge completed={row.is_completed} /> },
            ]}
          />
        </section>
      )}
    </>
  );
}

function Directory({ type }) {
  const config = {
    customers: {
      title: 'Клиенты',
      path: '/customers',
      icon: Users,
      columns: [
        { key: 'id', title: 'ID' },
        { key: 'name', title: 'Название' },
        { key: 'customer_type', title: 'Тип' },
        { key: 'contact_name', title: 'Контакт' },
        { key: 'address', title: 'Адрес' },
        { key: 'phone', title: 'Телефон' },
      ],
    },
    editions: {
      title: 'Издания',
      path: '/editions',
      icon: BookOpen,
      columns: [
        { key: 'id', title: 'ID' },
        { key: 'title', title: 'Название' },
        { key: 'sheet_count', title: 'Листы' },
        { key: 'circulation', title: 'Тираж', render: (row) => number(row.circulation) },
      ],
    },
    typographies: {
      title: 'Типографии',
      path: '/typographies',
      icon: Building2,
      columns: [
        { key: 'id', title: 'ID' },
        { key: 'name', title: 'Название' },
        { key: 'address', title: 'Адрес' },
        { key: 'phone', title: 'Телефон' },
      ],
    },
    authors: {
      title: 'Авторы',
      path: '/authors',
      icon: PenLine,
      columns: [
        { key: 'id', title: 'ID' },
        { key: 'full_name', title: 'ФИО' },
        { key: 'address', title: 'Адрес' },
        { key: 'phone', title: 'Телефон' },
        { key: 'bio', title: 'Описание' },
      ],
    },
  }[type];

  const [q, setQ] = useState('');
  const { data, loading, error, demoMode, reload } = useApi(`${config.path}?q=${encodeURIComponent(q)}`, [q]);
  const Icon = config.icon;

  return (
    <>
      <Toolbar title={config.title} subtitle="Справочник с поиском, сортировкой и процедурными действиями" onRefresh={reload} demoMode={demoMode} error={error}>
        <label className="search-box">
          <Search size={17} />
          <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Быстрый поиск" />
        </label>
      </Toolbar>
      <section className="directory-hero">
        <Icon size={28} />
        <div>
          <strong>{config.title}</strong>
          <span>{data?.length ?? 0} записей в текущей выборке</span>
        </div>
      </section>
      <DirectoryActions type={type} onDone={reload} />
      {loading ? <LoadingState /> : !data ? <ErrorState message={error} /> : (
        <section className="panel">
          <DataTable rows={data} columns={config.columns} />
        </section>
      )}
    </>
  );
}

function DirectoryActions({ type, onDone }) {
  const [message, setMessage] = useState('');
  const [customer, setCustomer] = useState({ customer_type_code: 'organization', name: '', contact_name: '', address: '', phone: '', fax: '' });
  const [address, setAddress] = useState({ id: '', address: '' });
  const [edition, setEdition] = useState({ id: '', circulation: '' });
  const [typography, setTypography] = useState({ name: '', address: '', phone: '' });
  const [author, setAuthor] = useState({ full_name: '', address: '', phone: '', bio: '' });

  async function submit(path, body, method = 'POST') {
    setMessage('');
    request(path, { method, body: JSON.stringify(body) })
      .then(() => {
        setMessage('Операция выполнена');
        onDone();
      })
      .catch((err) => setMessage(err.message));
  }

  if (type === 'customers') {
    return (
      <div className="forms-grid premium">
        {message && <div className="notice wide">{message}</div>}
        <form className="panel form-panel" onSubmit={(e) => { e.preventDefault(); submit('/customers', { ...customer, fax: customer.fax || null }); }}>
          <h3><Plus size={18} /> Добавить клиента</h3>
          <div className="field-row">
            <label>Тип<input value={customer.customer_type_code} onChange={(e) => setCustomer({ ...customer, customer_type_code: e.target.value })} /></label>
            <label>Название<input value={customer.name} onChange={(e) => setCustomer({ ...customer, name: e.target.value })} required /></label>
            <label>Контакт<input value={customer.contact_name} onChange={(e) => setCustomer({ ...customer, contact_name: e.target.value })} required /></label>
          </div>
          <div className="field-row">
            <label>Адрес<input value={customer.address} onChange={(e) => setCustomer({ ...customer, address: e.target.value })} required /></label>
            <label>Телефон<input value={customer.phone} onChange={(e) => setCustomer({ ...customer, phone: e.target.value })} required /></label>
            <label>Факс<input value={customer.fax} onChange={(e) => setCustomer({ ...customer, fax: e.target.value })} /></label>
          </div>
          <button className="primary lift" type="submit"><Plus size={17} />Добавить</button>
        </form>
        <form className="panel form-panel compact-form" onSubmit={(e) => { e.preventDefault(); submit(`/customers/${address.id}/address`, { address: address.address }, 'PATCH'); }}>
          <h3><PenLine size={18} /> Обновить адрес</h3>
          <label>Клиент ID<input value={address.id} onChange={(e) => setAddress({ ...address, id: e.target.value })} required /></label>
          <label>Новый адрес<input value={address.address} onChange={(e) => setAddress({ ...address, address: e.target.value })} required /></label>
          <button className="primary lift" type="submit">Обновить</button>
        </form>
      </div>
    );
  }

  if (type === 'editions') {
    return (
      <div className="forms-grid premium single">
        {message && <div className="notice wide">{message}</div>}
        <form className="panel form-panel" onSubmit={(e) => { e.preventDefault(); submit(`/editions/${edition.id}/circulation`, { circulation: Number(edition.circulation) }, 'PATCH'); }}>
          <h3><Gauge size={18} /> Обновить тираж</h3>
          <div className="field-row two">
            <label>Издание ID<input value={edition.id} onChange={(e) => setEdition({ ...edition, id: e.target.value })} required /></label>
            <label>Новый тираж<input value={edition.circulation} onChange={(e) => setEdition({ ...edition, circulation: e.target.value })} required /></label>
          </div>
          <button className="primary lift" type="submit">Обновить</button>
        </form>
      </div>
    );
  }

  if (type === 'typographies') {
    return (
      <div className="forms-grid premium single">
        {message && <div className="notice wide">{message}</div>}
        <form className="panel form-panel" onSubmit={(e) => { e.preventDefault(); submit('/typographies', typography); }}>
          <h3><Plus size={18} /> Добавить типографию</h3>
          <div className="field-row">
            <label>Название<input value={typography.name} onChange={(e) => setTypography({ ...typography, name: e.target.value })} required /></label>
            <label>Адрес<input value={typography.address} onChange={(e) => setTypography({ ...typography, address: e.target.value })} required /></label>
            <label>Телефон<input value={typography.phone} onChange={(e) => setTypography({ ...typography, phone: e.target.value })} required /></label>
          </div>
          <button className="primary lift" type="submit">Добавить</button>
        </form>
      </div>
    );
  }

  return (
    <div className="forms-grid premium single">
      {message && <div className="notice wide">{message}</div>}
      <form className="panel form-panel" onSubmit={(e) => { e.preventDefault(); submit('/authors', { ...author, address: author.address || null, phone: author.phone || null, bio: author.bio || null }); }}>
        <h3><Plus size={18} /> Добавить автора</h3>
        <div className="field-row">
          <label>ФИО<input value={author.full_name} onChange={(e) => setAuthor({ ...author, full_name: e.target.value })} required /></label>
          <label>Адрес<input value={author.address} onChange={(e) => setAuthor({ ...author, address: e.target.value })} /></label>
          <label>Телефон<input value={author.phone} onChange={(e) => setAuthor({ ...author, phone: e.target.value })} /></label>
        </div>
        <label>Описание<input value={author.bio} onChange={(e) => setAuthor({ ...author, bio: e.target.value })} /></label>
        <button className="primary lift" type="submit">Добавить</button>
      </form>
    </div>
  );
}

function Analytics() {
  const customerStats = useApi('/analytics/customer-stats');
  const typographyWorkload = useApi('/analytics/typography-workload');
  const openOrders = useApi('/analytics/open-orders');
  const completedOrders = useApi('/analytics/completed-orders');
  const loading = customerStats.loading || typographyWorkload.loading || openOrders.loading || completedOrders.loading;
  const error = customerStats.error || typographyWorkload.error || openOrders.error || completedOrders.error;
  const demoMode = customerStats.demoMode || typographyWorkload.demoMode || openOrders.demoMode || completedOrders.demoMode;

  if (loading) return <LoadingState />;
  if (!customerStats.data) return <ErrorState message={error} />;

  const workload = typographyWorkload.data.map((row) => ({ name: row.typography_name, orders: Number(row.orders_count) }));
  const customers = customerStats.data.map((row) => ({
    name: row.customer_name,
    total: Number(row.orders_count),
    open: Number(row.open_orders_count),
    completed: Number(row.completed_orders_count),
  }));

  return (
    <>
      <Toolbar
        title="Аналитика"
        subtitle="Представления ЛР6: нагрузка, клиенты, открытые и завершённые заказы"
        onRefresh={() => {
          customerStats.reload();
          typographyWorkload.reload();
          openOrders.reload();
          completedOrders.reload();
        }}
        demoMode={demoMode}
        error={error}
      />
      <div className="dashboard-grid">
        <section className="panel chart-panel wide">
          <div className="panel-heading">
            <div>
              <h3>Клиентская активность</h3>
              <p>Всего, открытые и завершённые заказы</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={290}>
            <BarChart data={customers}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d9e1e7" />
              <XAxis dataKey="name" stroke="#70828e" />
              <YAxis allowDecimals={false} stroke="#70828e" />
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #d9e1e7' }} />
              <Bar dataKey="completed" name="Завершено" stackId="a" fill="#2f9e75" radius={[0, 0, 8, 8]} />
              <Bar dataKey="open" name="В работе" stackId="a" fill="#f2b441" radius={[8, 8, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </section>
        <section className="panel chart-panel">
          <div className="panel-heading">
            <div>
              <h3>Типографии</h3>
              <p>Распределение заказов</p>
            </div>
          </div>
          <ResponsiveContainer width="100%" height={290}>
            <BarChart data={workload}>
              <CartesianGrid strokeDasharray="3 3" stroke="#d9e1e7" />
              <XAxis dataKey="name" stroke="#70828e" />
              <YAxis allowDecimals={false} stroke="#70828e" />
              <Tooltip contentStyle={{ borderRadius: 12, border: '1px solid #d9e1e7' }} />
              <Bar dataKey="orders" name="Заказы" fill="#6d5dfc" radius={[10, 10, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </section>
        <section className="panel">
          <h3>Открытые заказы</h3>
          <DataTable rows={openOrders.data} columns={[
            { key: 'order_id', title: '№' },
            { key: 'customer_name', title: 'Клиент' },
            { key: 'edition_title', title: 'Издание' },
            { key: 'received_at', title: 'Принят', render: (row) => formatDate(row.received_at) },
          ]} />
        </section>
        <section className="panel">
          <h3>Завершённые заказы</h3>
          <DataTable rows={completedOrders.data} columns={[
            { key: 'order_id', title: '№' },
            { key: 'customer_name', title: 'Клиент' },
            { key: 'edition_title', title: 'Издание' },
            { key: 'completed_at', title: 'Завершён', render: (row) => formatDate(row.completed_at) },
          ]} />
        </section>
      </div>
    </>
  );
}

function CommandPalette({ active, setActive }) {
  const [query, setQuery] = useState('');
  const matches = navItems.filter((item) => `${item.label} ${item.hint}`.toLowerCase().includes(query.toLowerCase()));
  return (
    <div className="command-card">
      <Command size={17} />
      <input value={query} onChange={(e) => setQuery(e.target.value)} placeholder="Быстрая навигация: заказы, клиенты, аналитика..." />
      {query && (
        <div className="command-results">
          {matches.map((item) => {
            const Icon = item.icon;
            return (
              <button key={item.id} className={active === item.id ? 'active' : ''} onClick={() => { setActive(item.id); setQuery(''); }}>
                <Icon size={16} />
                <span>{item.label}</span>
                <small>{item.hint}</small>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}

function App() {
  const [active, setActive] = useState('overview');
  const item = navItems.find((entry) => entry.id === active) ?? navItems[0];
  const CurrentIcon = item.icon;

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark"><Database size={24} /></div>
          <div>
            <strong>Publishing DB</strong>
            <span>PostgreSQL control room</span>
          </div>
        </div>
        <nav>
          {navItems.map((nav) => {
            const Icon = nav.icon;
            return (
              <button key={nav.id} className={active === nav.id ? 'active' : ''} onClick={() => setActive(nav.id)}>
                <Icon size={18} />
                <span>{nav.label}</span>
                <small>{nav.hint}</small>
              </button>
            );
          })}
        </nav>
        <div className="side-card">
          <ShieldCheck size={20} />
          <strong>PL/pgSQL guard</strong>
          <span>Все критичные операции идут через процедуры с проверками.</span>
        </div>
      </aside>
      <main>
        <header className="topbar">
          <div>
            <span className="eyebrow"><CurrentIcon size={16} /> информационная система издательства</span>
            <h1>{item.label}</h1>
          </div>
          <div className="topbar-tools">
            <CommandPalette active={active} setActive={setActive} />
            <span className="connection">API {API_URL}</span>
          </div>
        </header>
        {active === 'overview' && <Overview setActive={setActive} />}
        {active === 'orders' && <Orders />}
        {active === 'customers' && <Directory type="customers" />}
        {active === 'editions' && <Directory type="editions" />}
        {active === 'typographies' && <Directory type="typographies" />}
        {active === 'authors' && <Directory type="authors" />}
        {active === 'analytics' && <Analytics />}
      </main>
    </div>
  );
}

createRoot(document.getElementById('root')).render(<App />);
